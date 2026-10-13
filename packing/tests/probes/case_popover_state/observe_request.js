/** Observe one real fetch after its response consumer's microtasks, without a timer.
 * @param {{url: string}} options
 */
({ url }) => {
  const original = globalThis.fetch;
  /** @type {() => void} */
  let complete = () => {};
  const completed = new Promise((resolve) => {
    complete = () => resolve(undefined);
  });
  const consumed = () => {
    const channel = new MessageChannel();
    channel.port1.onmessage = () => {
      channel.port1.close();
      channel.port2.close();
      complete();
    };
    // The next task follows all callbacks consuming the completed response or error.
    channel.port2.postMessage(null);
  };
  globalThis.fetch = async (input, init) => {
    const requested =
      input instanceof Request ? input.url : new URL(String(input), document.baseURI).href;
    const response = await original(input, init);
    if (requested === url) {
      if (!response.ok) {
        consumed();
      } else {
        const text = response.text.bind(response);
        response.text = async () => {
          try {
            return await text();
          } finally {
            consumed();
          }
        };
      }
    }
    return response;
  };
  return { completed };
};
