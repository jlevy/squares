.PHONY: verify reproduce reproduce-only clean

verify:
	bash ./verify_archived.sh

reproduce:
	bash ./verify_4p468292.sh

reproduce-only:
	bash ./reproduce_certificate.sh

clean:
	rm -f verify_certificate verify_certificate_bigint generate_certificate square17_lb_4p468292.cert
