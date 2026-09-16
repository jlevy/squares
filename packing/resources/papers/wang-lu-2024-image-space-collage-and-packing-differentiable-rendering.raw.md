                                         Image-Space Collage and Packing with Differentiable Rendering
                                         ZHENYU WANG, Shenzhen University, China
                                         MIN LU*, Shenzhen University, China
arXiv:2406.04008v3 [cs.GR] 26 May 2025




                                         Fig. 1. The ‘SIGGRAPH’ example is created using our method: (S) demonstrates the fundamental approach with good shape containment, non-overlap, and
                                         uniform distribution; (I) incorporates padding around geometric elements; (G-G) illustrates the smooth transition from axis-based initialization to final filling;
                                         (R) showcases collages with stripe blocks; (A) highlights packing within a shape with a downward force; and (P, H) display open packing arrangement with a
                                         downward force.

                                         Collage and packing techniques are widely used to organize geometric shapes 1 Introduction
                                         into cohesive visual representations, facilitating the representation of visual Assembling and collaging geometric elements to encapsulate visual
                                         features holistically, as seen in image collages and word clouds. Traditional
                                                                                                                          features provide a unified representation, which has been instrumental
                                         methods often rely on object-space optimization, requiring intricate geometric
                                         descriptors and energy functions to handle complex shapes. In this paper, we
                                                                                                                          in creating intriguing visual designs and artworks, such as circular
                                         introduce a versatile image-space collage technique. Leveraging a differentiable packing maps to show the thematic topic [4], word clouds for engaging
                                         renderer, our method effectively optimizes the object layout with image-space overview of texts [33], or digital collages of photos [39]. Despite its
                                         losses, bringing the benefit of fixed complexity and easy accommodation of popularity across various fields, the task of packing elements into
                                         various shapes. Applying a hierarchical resolution strategy in image space, our given regions presents significant challenges. Numerous techniques
                                         method efficiently optimizes the collage with fast convergence, large coarse have been proposed to address this task, with the majority of existing
                                         steps first and then small precise steps. The diverse visual expressiveness of collage methodologies concentrating on object-space optimization [18,
                                         our approach is demonstrated through various examples. Experimental results 28, 37, 46]. In object space, measuring the fit between geometric objects
                                         show that our method achieves an order of magnitude speedup performance often involves designing geometric descriptors and energy functions
                                         compared to state-of-the-art techniques.
                                                                                                                            specifically tailored to address the complexity of the objects’ shapes.
                                         CCS Concepts: • Computing methodologies → Shape analysis; Image-   Object-based techniques frame
                                         based rendering.                                                 collages as a geometric constraint
                                                                                                                            satisfaction problem, accompa-
                                         Additional Key Words and Phrases: Collage, Differetiable Rendering, Image
                                         Space
                                                                                                                   nied by certain limitations. First,
                                                                                                                            geometric shapes usually need
                                         ACM Reference Format:                                                         careful analysis to enable effec-
                                         Zhenyu Wang and Min Lu*. 2025. Image-Space Collage and Packing with tive shape matching [18, 41]. For instance, reducing the overlap be-
                                         Differentiable Rendering. In Proceedings of (SIGGRAPH Conference Papers’ 25). tween shapes 𝐴 and 𝐵 necessitates the shape descriptors for their
                                         ACM, New York, NY, USA, 11 pages. https://doi.org/10.1145/3721238.3730690
                                                                                                                                       boundaries (𝜕𝐴 and 𝜕𝐵). Additionally, geometric descriptors often lack
                                                                                                                                       generalizability. For instance, some works necessitate shapes with
                                         * Corresponding author: Min Lu (lumin.vis@gmail.com).
                                                                                                                                       curvature and are unable to handle open shapes [18]. Some others
                                                                                                                                       are limited to fitting containers within convex boundaries [46]. Fur-
                                         Permission to make digital or hard copies of all or part of this work for personal or thermore, the optimization process in object-based approaches can be
                                         classroom use is granted without fee provided that copies are not made or distributed for
                                         profit or commercial advantage and that copies bear this notice and the full citation on the computationally intensive, depending on the scale and complexity of
                                         first page. Copyrights for components of this work owned by others than the author(s) the objects involved.
                                         must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to
                                         post on servers or to redistribute to lists, requires prior specific permission and/or a fee.
                                                                                                                                         In this work, we advocate a paradigm shift in shape collage tech-
                                         Request permissions from permissions@acm.org.                                                 niques by transitioning the geometric packing optimization from the
                                         SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada                     object space to the image space. The core idea is to cast the geometric
                                         © 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM.             representation and their spatial relationships onto a grid of pixels,
                                         ACM ISBN 979-8-4007-1540-2/2025/08
                                         https://doi.org/10.1145/3721238.3730690                                                       which are with fixed and object-independent complexity. Leveraging

                                                                                                                                    SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
2 •   Zhenyu Wang and Min Lu


the power of differentiable rendering [22], our method enables gradient dots and lines in the cells. Dalal et al. [3] proposed the Sum of Squared
backpropagation from image-space losses to geometric objects, effec- Distance metric for even distribution of the primitives with spatial
tively steering the collage optimization process from the discrete image extent. Further, Reinert et al. [34] facilitated real-time computation of
space. Operating in image space facilitates a hierarchical resolution the sum of squared distance using GPUs and allowed user customiza-
approach to dynamically manage the precision of these image-space tion by example. Unlike these methods with tiles and cell adjustments,
losses. The collage process begins with low-resolution losses to facili- our work optimizes primitives without global tessellation constraints.
tate large, bold adjustments and progressively increases resolution for Primitives can overlap initially with overlaps, like the ‘G’ in Figure 1,
finer refinements. This hierarchical approach significantly accelerates and fit into open-shaped containers as shown in the ‘PH’ example of
the computation, achieving an order-of-magnitude speedup compared Figure 1.
to state-of-the-art methods.                                                 Another related research topic is image collection, also called photo
   The key strength of our technique is its ability to bypass complex collage, which deliberately allows occlusions and blends. Many ap-
object problem-solving by leveraging the inherent advantages of image- proaches have been proposed [36, 44]. For example, ShapeCollage [38]
space optimization. This enables it to fit various geometric shapes into supports to interactively make a collage of photos with overlapping
almost any desired target shapes. As shown in Figure 1, our method among photos. Rother et al. [36] allowed for soft intersection among
demonstrates its versatility by supporting a wide range of design photos. Goferman et al. [5] fused parts of photos into one whole im-
configurations. These range from core space filling, as seen in ‘S’, age. Huang et al. [11] matched multiple cutouts from the Internet to
to packing designs influenced by gravity effects in ‘A’, open-region compose a thematic figure. Liu et al. [23] extracted salient regions
packing exemplified by ‘H’, and complex shapes, such as the white and proposed a correlation-preserved photo collage. Pan et al. [30]
stripe blocks in ‘R’. Another advantage of our method, which employs presented a content-based visual summarization technique for image
gradual descent, is the smooth animation generated during the collage collections. More recently, instead of matching existing photos, Lee et
and packing process, as illustrated by the ‘G’s in Figure 1. In the al. [20] generated collage artwork via reinforcement learning based on
evaluation, we compared our collage method against state-of-the-art a given target image and materials, considering scores such as diversity,
baselines. Results show that our method significantly surpasses the aesthetics, etc.
baselines in visual quality. More importantly, our method achieves a         Text Filling Texts can be regarded as special geometric shapes. Con-
remarkable improvement in computational efficiency and scalability, siderable research has focused on arranging words to create text-based
with gains on the order of magnitude.                                     visual design and word art. Word clouds, popular for visually represent-
                                                                          ing words in a compact layout, have been extensively studied [7, 35, 42].
                                                                          Tools such as Wordle [27] help with the easy creation of word clouds.
2 Related Work                                                            Cui et al.[2] proposed a dynamic force-directed model for word cloud
The collage and packing problem have been widely studied [48], in- layout, which preserves semantic context over time. Wu et al.[47] uti-
cluding 3D object arrangement [10, 25, 55]. Below, we mainly review lized seam carving to optimize word cloud layouts. Beyond traditional
the research work related to 2D approaches.                               word clouds, researchers have explored filling words within specific
   Collage In 2D space, collage can be broadly categorized into two shapes. Paulovich et al. [32] introduced a cutting-stock optimization
types: geometric graphics and images. Circular packing, exemplified by method that optimizes the arrangement of words to maximize space
the work of Wang et al. [45], is a common paradigm, with new circles utilization within shapes. ShapeWordle [46] took a different approach
added to the outer periphery of existing ones. Several variations of cir- by utilizing the Archimedean spiral to accommodate irregular shapes,
cular packing have been developed, such as single-axis packing [24, 53], resulting in visually appealing word cloud compositions. MetroWor-
generative treemap [43], and hierarchical packing strategy [13]. Irreg- dle [21] combined word clouds with maps, incorporating collision
ular shapes have also been considered, with methods like arclength detection for geotags. Chi et al. [1] presented temporally morphable
descriptor matching [18] and autocomplete-based optimization [9]. word cloud technology that allows word clouds to undergo smooth
Saputra et al. [37] represented objects as mass element meshes and shape transformations over time. Xie et al. [49] proposed animating
used the repulsion forces between neighboring meshes to even out the word cloud for emotional expression.
negative space. Calligraphic packing, employed for letter composition, Some other works support interactive word cloud customization.
has been explored by Xu et al.[50] and enhanced for legibility by Zou For example, Koh et al.[17] introduced an interactive interface to facil-
et al.[56]. Those collage works deliberately describe primitives with itate user-driven word manipulation within word clouds. Jo et al. [15]
geometric parameters, and then optimize over those parameters. Our introduced WordPlus, which expands the interaction of Wordle by
approach avoids the need for complex geometric computation and the incorporating pen and touch interactions. Additionally, Surazhsky et
use of task-specific descriptors within the geometry space. Working al.[40] proposed a method for text layout on 3D objects. Maharik et
in image space, our approach can be easily adapted for a variety of al.[26] used streamline-based techniques to arrange words artistically.
applications.                                                             Zhang et al. [52] introduced a word arrangement method that arranges
   There is a another bunch of works achieving visually pleasing and theme-related words at the salient areas. Xu et al.[51] introduced a
balanced packing via a top-bottom manner, which divides the canvas tone-based ASCII art generation method.
into region cells via tessellation and then adjusts the placement of         Unlike object arrangement guided by space-filling curves or collision
primitives within the cells. Kim and Pellacini [16] proposed an explicit detection, our framework utilizes image-based loss for flexible word
packing energy function to optimize tiles for compact layouts. Hiller fitting, accommodating loose compositions like force-attracted filling
et al. [8] optimized the centroid placement of small objects such as in a non-closed constrained boundary.

SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
                                                                                                          Image-Space Collage and Packing with Differentiable Rendering   • 3


                                                                                            epoch. First, each geometric item undergoes a geometric transforma-
                                                                                            tion applied to its control points 𝑃, resulting in:

                                                                                                       P𝑖′ = r𝑖 · (P𝑖 ⊙ s𝑖 ) + t𝑖 , ∀𝑖,                 (2)
                                                                                   where geometric items are continuously adjusted by parameters of
                                                                                t (translation), s (scaling), and r (rotation). Geometric items are then
                                                                                rasterized into an image 𝐼ˆ at resolution 𝑤 ×ℎ by differentiable rendering.
                                                                                The container image is rasterized into a target image 𝐼𝐶 , where the
                                                                                interior is black and the exterior is white. A series of image-based loss
Fig. 2. Image-space collage and packing framework: starting with initialized 2D functions are calculated:
geometric items and their transformations, image-space losses are computed
between the rasterized image and the target shape of the collage container                             L (𝐼ˆ(𝑥, 𝑦; P), 𝐼𝐶 ).                     (3)
across a hierarchy of image resolutions. These losses are then used to itera-
tively update the transformation parameters, refining the arrangement of the    Following an  update via gradient   descent, the image loss is back-
geometric items.                                                              propagated to the parameters within the geometric transformation,
                                                                                            updated as:

3   Preliminaries                                                                                         𝜕L         𝜕L
                                                                                                             t, s, r := t − 𝜂
                                                                                                              , s−𝜂      , r−𝜂
                                                                                                                               𝜕L
                                                                                                                                   .            (4)
   Collage Problem. Given a set of 2D geometric items 𝐺 = {𝑔1, 𝑔2, . . . , 𝑔𝑛 },                           𝜕t         𝜕s        𝜕r
the goal of collaging is to arrange them in a geometric container region         Over the optimization process, the image-space loss is calculated
𝐶, where each shape 𝑠𝑖 may undergo geometric transformations, in- among raster images at multiple levels of resolutions, starting with a
cluding translate (t), scale (s) and rotate (r). The optimization problem low resolution and gradually moving to higher resolutions. The trans-
is formulated as:                                                             formation parameters are updated iteratively until the arrangement of
                                                                              items converges to an optimal solution.
                                   min                           L (𝐺, 𝐶, t, r, s),   (1)
                t1 ,t2 ,...,t𝑛 ,r1 ,r2 ,...,r𝑛 ,s1 ,s2 ,...,s𝑛                              4.1   Initialization
   where L quantifies the arrangement quality within the container 𝐶. We propose a skeleton-based initialization method for distributing
Non-overlapping and shape containment are two basic constraints: geometric items within the shape container. We use the Medial Axis
                                                                          Transform (MAT)[19] to extract the skeleton of the target shape and
     Shape Containment: 𝐺𝑖 (t𝑖 , r𝑖 , s𝑖 ) ⊆ 𝐶, ∀𝑖 = 1, 2, . . . , 𝑛      calculate the medial width (distance to the nearest boundary point). As
                                                                          illustrated in Figure3, visual elements are distributed along the medial
     Non-overlap: 𝐺𝑖 (t𝑖 , r𝑖 , s𝑖 ) ∩ 𝐺 𝑗 (t 𝑗 , r 𝑗 , s 𝑗 ) = ∅, ∀𝑖 ≠ 𝑗
                                                                          axis, with larger elements positioned at points with greater medial
   Vector Representation. We adopt a uniform vector representation width. This approach ensures an even distribution of elements within
for 2D geometric item of any shape. For each item, a closed area with the shape, making it especially effective for tubular shapes. Note that
𝑁 cubic Bézier curves {(𝑝𝑥 , 𝑝 𝑦 )}𝑖=13𝑁 is initialized and fitted to the our method is robust to initialization. In Section 5, we show it can
silhouette of the item via differentiable rendering. The parameter 𝑁 effectively handle poor initialization conditions as discussed in [28].
controls the shape’s granularity. In our examples, we set 𝑁 = 20 to
provide a balance of efficiency and geometric precision.
   Differentiable Rendering. Rasterization can be considered as a map-
ping (or called scene function 𝐼 ) from the vector graphics to a 2D
pixel grid, denoted as 𝐼 (𝑥, 𝑦; Θ), where (𝑥, 𝑦) is the position of a pixel
in the 2D grid, and Θ represents the vector graphic parameters (e.g.,
control points of a Bézier curve). Differentiable rendering is a class
of techniques that makes the rasterization process differentiable. Dif- Fig. 3. MAT-based position initialization: with the detected medial axes and
ferentiable rendering of vector graphics allows the backpropagation their nearest associated widths to the boundary (left), visual elements are
from the image domain to the vector graphics domain. Specifically, initialized in the way that larger ones are placed on axes with larger medial
the scene function 𝐼 is differentiated with respect to the parameters widths (right).
Θ. Several implementations exist, such as those using differentiable
neural networks to approximate rasterization [29, 54]. In this work, 4.2 Image-based Loss
we adopt the differentiable rendering approach by Li et al.[22], which We designed the image-space function to ensure two essential require-
leverages the observation that pixel colors become continuous after ments, i.e., shape containment and non-overlapping.
anti-aliasing.                                                                Shape Containment. We propose a spatial
                                                                            penalty mask to enhance the basic image mean
4 Image-space Collage                                                       square error loss (MSE loss) by encouraging ele-
Given the collage container 𝐶, the set of 2D geometric items 𝐺 are ments to full fill the target shape. Geometric items
iteratively optimized into a collage, as illustrated in Figure 2 for each are rendered into black and white image 𝐼ˆ𝑏&𝑤 . The

                                                                                                   SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
4   •   Zhenyu Wang and Min Lu


penalty mask 𝑊 ∈ R𝑤×ℎ assigns a small penalty (𝑤𝑖 𝑗 = 1) for pixel initial computations and progressively increasing to a high resolution
difference within the target container region and a large penalty (600 × 600) for refinement. Further details are discussed in Section 6.1.
(𝑤𝑖 𝑗 = 100) for difference outside. The Weighted Mean Square Er-                              Hierarchical resolution strategy
ror (WMSE) between differentiable rasterized image 𝐼ˆ and the target




                                                                                   Collage Quality
                                                                                         6002
image 𝐼 is then calculated as:                                                 2002 4002
                                                                                                     1002
                                   1                                           502
                                                        2                                                     50x50
                 Lcontainment =       𝑊 ⊙ 𝐼ˆ𝑏&𝑐 − 𝐼𝐶 .                 (5)                                                 200x200
                                 𝑤 ·ℎ                                                  Time Cost
                                                                                                                                              600x600
   Non-overlapping. In image space, detecting
overlap among elements is straightforward and                              Fig. 4. Trade-off between collage quality and computation time for different
avoids geometric computations. Overlap is esti-                            image resolutions. Note that the three collages on the right have been resized
mated by rendering all vector primitives with a fixed                      for better visualization of quality differences and do not reflect their original
transparency 𝜏, and and counting pixels whose trans-                       resolution.
parency values deviate from 𝜏, indicating overlapping regions, where
I is an indicator function for the transparency condition, and 𝑝 is a
pixel of the image:                                                        5 Results
                                                                           Building on the core image-space collage method introduced earlier,
                                  1 ∑︁                                     Figure 13 presents examples of visual collage designs, spanning from
                    Loverlap =           I(𝑇 (𝑝) > 𝜏).                 (6)
                                𝑤 ·ℎ 𝑝                                     intricate vector icons to hand-drawn sketches. Figure 14 demonstrates
                                                                           how the collage technique integrates seamlessly with images. Below,
   Even Distribution. The two loss functions dis-                          we explore how this technique can be extended to support a diverse
cussed above constrain visual elements within the                          range of use cases.
target shape and prevent overlap, but uneven distri-                          Force Attraction Our method can be seamlessly integrated with
bution may still occur, negatively impacting overall                       force-directed techniques. For example, by defining an attracting or
visual quality. To address this, we propose a uniform                      repelling force source, the distance between visual elements and the
loss Luniform . This is achieved through differentiable image dilation force source can be computed as a loss function to influence the move-
(𝑑), using a series of convolution kernels with increasing bandwidths ment of the elements. This approach enables controlled attraction or
(starting at five pixels, incrementing by six pixels per step) to approxi- repulsion of elements based on the specified force field. As shown in
mate a distance field. As defined in Equation 7, Luniform is computed Figure 5 (left), a packing layout such as a circular or horizontal layout
as the weighted sum of pixels (𝑝) in non-occupied regions within the can be achieved using a central force point or a linear downward force.
collage container. The weights (𝑤) are assigned based on kernel band- Additionally in Figure 5 (right), elements can be attracted into the
widths, increasing for larger kernels. Larger dilations highlight broader mask by the force attraction with the collage mask.
gaps and are assigned higher weights, while smaller dilations receive
lower weights. This approach emphasizes larger spaces, prioritizing
their reduction to achieve a more uniform distribution. The equation
is as follows:
                                         ∑︁ ∑︁
                           Luniform =              𝑤𝑑 .                      (7)
                                          𝑑    𝑝

  The overall loss function, shown in Equation 8, uses weights 𝛼, 𝛽,
and 𝛾 set to 3e3, 8e4, and 5e-4 respectively, to determine the relative
contributions of the factors in the optimization process:

               L = 𝛼 Lcontainment + 𝛽Loverlap + 𝛾 Luniform .                 (8)
                                                                         Fig. 5. Packing examples with attracting forces: (left) our technique integrates
                                                                         a centripetal or downward force to pack elements efficiently within an open
4.3 Hierarchical Image Resolution                                        area; (right) using a collage container, elements are first attracted and confined
The resolution of the image 𝐼ˆ ∈ 𝑅 𝑤×ℎ plays a crucial role in balancing within specific shapes.
loss precision and computational efficiency, as is also observed in         Animation Effects The gradual optimization process of our col-
general image analysis tasks [6]. Figure 4 illustrates this trade-off. lage technique produces a side effect: captivating animation effects,
Low-resolution images enable faster loss computation but provide distinguishing it from search-and-match algorithms [18]. As shown
lower precision in detecting overlap and containment, resulting in in Figure 6(top), the star glyphs are initialized on the top line and
reduced collage quality. Conversely, high-resolution images enhance fall by a downward attracting force, creating an animation effect of
precision and overall collage quality but come with significantly higher ‘falling down’. In Figure 6(bottom), by the MAT-based initialization, the
computation costs. To balance precision and efficiency, we adopt a visual elements move outwards to fit in the shape of the US boundary,
hierarchical strategy: starting with a low resolution (50×50) to expedite creating an animation effect of ‘expanding’.

SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
                                                                                              Image-Space Collage and Packing with Differentiable Rendering   • 5


                                                                               by a hand-drawn circle, with colors indicating prize categories, creat-
                                                                               ing a clear and engaging representation of the dataset. In this example,
                                                                               a downward force is integrated to create visual effect of sedimentation.




Fig. 6. Gradual optimization creates animation effects: (top) an expanding
animation effect, (bottom) a falling down animation effect.                Fig. 8. Unit data visualization examples: (left) coffee production infographic, in
                                                                           which each coffee bean is a county that produces coffee, and its size encodes
                                                                           the coffee production. (right) Nobel prize winners in the US, each Nobel winner
                                                                           is represented as a circle, whose color indicates its category.


                                                                               6   Evaluation
                                                                               In this section, we first report the results of the ablation study and then
                                                                               elaborate on the comparison between our method and state-of-the-art
                                                                               methods.

                                                                                    Metrics of Collage Quality. We used three metrics to quantitatively
                                                                                 measure the quality of the generated collages. The first metric is
                                                                                 adopted from exiting work [46], and additional two metrics are added
                                                                                 to quantify the overlaps among objects and the target shape: (1) Layout
Fig. 7. Word clouds that pack words into animal shapes: from left to right, a Coverage (LC): it is quantified as the proportion between the number
vertically-aligned collage in the shape of a seahorse, a horizontally-aligned of pixels in the object area (i.e., words in the clouds) and the number
collage in the shape of a cat, and a loosely horizontally-aligned collage in the
                                                                                 of pixels in the non-object area inside the target shape, the bigger the
shape of a bird.
                                                                                 better; (2) Object Overlap (OO): it is quantified as the ratio of pixels in
                                                                                 the overlap areas between objects to the total number of pixels in the
                                                                                 target shape; (3) Exceeding Area (EA): it is quantified as the ratio of
    Graphic Text Blending Our method seamlessly integrates text pixels that exceed the target shape to the total number of pixels in the
and graphics, enabling cohesive and visually appealing compositions. target shape.
As illustrated in Figure 7, our technique is used to generate word
clouds (also known as wordles), where words of varying font sizes are 6.1 Ablation Study
arranged to form specific shapes, creating a balanced and engaging
                                                                                    Ablation on Uniform Loss. We investigated the impact of uniform
design. In Figure 14, we show examples of blending texts within image
                                                                                 loss on collage quality, and quantified the Layout non-Uniformity (L-nU)
regions with low saliency. This ensures that less prominent areas are
                                                                                 as the averaged distance square of non-object pixels to their nearest
utilized effectively, enhancing the overall layout while maintaining
                                                                                 objects. As shown in Figure 9, without the uniform loss, the elements
the visual emphasis on key elements.
                                                                                 are less evenly distributed. For example, in the highlighted regions,
    Data Visualization. Our method supports unit visualization, where
                                                                                 collages without uniform loss leave noticeable gaps in other areas,
each visual element represents a data item [31]. In Figure 8 (left), the
                                            1                                    which disrupt the overall balance and aesthetic consistency of the
Country Coffee Production dataset is visualized, with each coffee-
                                                                                 design.
producing country represented by a coffee bean. The size of the bean
encodes the country’s coffee production, and the uniform scaling pa-
                                                                                    Ablation on Image Resolution Strategies. We conducted an ablation
rameter s ensures accurate area-based encoding without loss of fidelity.
                                                                                 study to evaluate the impact of different image resolution strategies
Figure 8 (right) illustrates a bar-like sedimentary visualization of the
                                                                                 on performance. The study examined eight constant resolution ap-
Nobel Prize Winners in the US from 19022 . Each winner is represented
                                                                                 proaches, ranging from 50 to 1200 (shown in Table 1), and two hierar-
                                                                                 chical resolution strategies 100 + 600 and 50 + 200 + 600.
1 https://www.kaggle.com/datasets/michals22/coffee-dataset                          The evaluation was conducted under four conditions, packing 100
2 https://www.kaggle.com/datasets/joebeachcapital/nobel-prize                    elements into four different collage shapes to assess the effectiveness

                                                                                       SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
6 •        Zhenyu Wang and Min Lu


                                                                                                     Table 1. Comparison of collage quality and time cost over resolution strategies:
                                                                                                     time is the cost of 200 optimizing epochs.
                                                         Layout Uniformity




                                                                                                        Resolution      Coverage (LC) Overlap (OO) Exceed (EA)          Time (s)
                                                                                                          50x50            69.67%        2.72%        1.11%              12.90
                                                                                                         100x100           65.60%        0.68%        0.33%              13.41
 w/o Uniform Loss        with Uniform Loss     w/o Uniform Loss                  with Uniform Loss       200x200           73.43%        0.42%        0.07%              15.44
   L-nU: 67.38             L-nU: 50.32           L-nU: 220.16                       L-nU: 58.82          400x400           67.55%        0.08%        0.01%              22.36
                                                                                                         600x600           70.77%        0.11%        0.00%              32.54
Fig. 9. Comparison of collages with and without the uniform loss: with uniform                           800x800           72.23%        0.12%        0.00%              52.42
loss, the elements (e.g., texts on the right example) exhibit a more evenly                             1000x1000          71.16%        0.05%        0.00%              76.04
distributed arrangement.                                                                                1200x1200          69.39%        0.01%        0.00%              99.76
                                                                                                         100+600           51.47%        0.02%        0.00%              18.51
                                                                                                       50+200+600          60.73%       0.01%↓        0.00%             20.74 ↓




                                                                                                     both methods, while being significantly faster. Specifically, our method
                                                                                                     generates the example in six minutes, compared to over 700 minutes
                                                                                                     for PAD. Against Minkowski Penalty, our method demonstrates similar
                                                                                                     time efficiency for the tested examples, around 100 elements. As the
                                                                                                     number of elements increases, the optimization time for Minkowski
      50           100        200        600         1200                    100_600   50_200_600    Penalty would grow longer due to its O (𝑛 2 ) time complexity for ar-
                                                                                                     ranging constraint pairs.
Fig. 10. Result samples generated using different resolution strategies: the left
five use constant resolutions from low to high, while the right two employ
hierarchical resolution strategies.


of resolution strategies across varying shape complexities. All exam-
ples are generated over 200 optimization epochs. For the hierarchical
resolution strategy, the epochs were evenly distributed across each
resolution level. Figure 10 shows collage samples generated using dif-
ferent image resolutions. In the figure, the target shapes are shown in
yellow, visual objects in gray, overlaps between visual objects (OO) in
red, and areas exceeding the target shapes (EA) in blue.
   The averaged results are summarized in Table 1, revealing clear
trade-offs between resolution strategy and time cost. As can be seen,
collage quality improves as the resolution increases. The constant high-
resolution 600×600 achieved high metric scores but incurred significant
computational overhead. In contrast, the hierarchical strategies, espe-
cially 50 + 200 + 600, demonstrated more balanced performance. They
delivered competitive metric results while maintaining lower time
costs, highlighting their efficiency in managing resolution adaptively. Fig. 11. Examples and their time cost generated by our method and others:
                                                                                                     (top) with PAD [18], and (bottom) with Minkowski Penalty [28].

6.2        Comparison Experiment                                           Quantitative Comparison. We performed a quantitative comparison
We compared our method with four existing methods: PAD [18],           between     our method and PAD, ShapeWordle and ShapeCollage, based
Minkowski Penalty [28], ShapeWordle [46], and ShapeCollage [38].       on   the  three collage quality metrics. We tested ShapeWordle and our
ShapeWordle is designed specifically for text, while ShapeCollage is   method      on two  target shapes (‘flower’ and ‘leaf’ in Figure 12) from
                                                                                                      3
tailored for rectangular images. Due to the limitations of these meth- the ShapeWordle website . PAD and our method were tested using
ods in handling general geometric shapes, we performed one-on-one      two   examples   from   the PAD   work [18] (‘Australia’ and ‘Letter P’). For
comparisons between our approach and each baseline in specific sce-    comparison     with  ShapeImage,   two general target shapes were chosen,
narios.                                                                ‘Moon’     and ‘Fish’. Table 2  summarizes   the three metrics of different
                                                                       methods across the six examples.
   Qualitative Comparison. We compared our method with PAD and
Minkowski Penalty, both designed for generating shape collages. As
shown in Figure 11, our method delivers visually comparable results to 3 https://www.shapewordle.com/

SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
                                                                                                                  Image-Space Collage and Packing with Differentiable Rendering   • 7


                                          Table 2. Comparison between our method and three baselines on the six examples in Figure 12.

    XXX
             XXMethods                            Fig. 12 Flower             Fig. 12 Leaf      Fig. 12 Letter P    Fig. 12 Australia      Fig. 12 Moon            Fig. 12 Fish
     Metrics       XXX                          ShapeW.       Ours        ShapeW.      Ours    PAD       Ours      PAD       Ours       ShapeC.     Ours       ShapeC.      Ours
     Layout Coverage (LC)                         0.25       0.28 ↑         0.18      0.29 ↑   0.94      0.80      0.91      0.75         0.67     0.86 ↑        0.67      0.87 ↑
   Object Overlap (OO) ×10 −3                       0           0             0        0.02    33.83 0.14 ↓        55.30    0.30 ↓       41.44     0.09 ↓       40.04      0.08↓
   Exceeding Area (EA)×10 −3                        0           0             0          0     7.17       0↓       21.84      0↓         18.31        0          7.86        0↓


                                                                                 incorporate imaginative concepts, thereby expanding the possibilities
          PAD [18]                       Ours                                        Ours
                                                           ShapeWordle [46]
                                                                                 for expressive and engaging visual design.
                                                                                    Link with Image Generation Models In light of the advancements
                                                                                 made, there are several promising directions for future research and
                                                                                 development. One potential avenue is the exploration of interactive
                                                                                 interfaces for target image-space editing in visualization creation. By
                                                                                 providing users with intuitive editing and controls in the target image,
                                                                                 they can directly manipulate and refine the visual elements in return,
                                                                                 allowing for a more interactive and iterative design process. Designing
                                                                                 an interactive system for collage authoring would be an interesting
                                                                                 work in the future. A more promising avenue is to import text-driven
                                                                                 editing for collage design based on a text-to-image foundation model
                     ShapeCollage [38]                                        Ours
                                                                                 [12][14].
                                                                                    Element Initialization. In this work, we experimented with one prim-
                                                                                 itive initialization method, MAT-based. It is important to note that
                                                                                 different primitive initialization methods can be suitable for different
                                                                                 conditions, depending on the specific requirements and constraints
                                                                                 of the application. For example, the MAT-based initialization proves
Fig. 12. Comparison between our method and three existing methods: yellow effective for shapes with varying widths, such as tubes and necks.
areas are the target shape, red areas are where visual objects overlap, and blue As seen in the ‘tail of seahorse’ of Figure 7, our experiments validate
areas are where visual objects exceed the target shape.                          the promising results achieved through the MAT-based initialization
                                                                                 technique. However, the MAT-based method is not optimal for target
                                                                                 shapes with round bellies. Potential future work is to study adaptive
                                                                                 primitive initialization techniques that automatically suggest initial
    Figure 12 uses the same visual encoding as Figure 10. As can be seen,
                                                                                 visual primitives based on the geometric features of the target shape.
compared to ShapeWordle, our method consistently demonstrates su-
                                                                                 This would enhance the efficiency and accuracy of the initialization
perior performance in Layout Coverage (LC). In both the ‘leaf’ and
                                                                                 process, leading to better adaptation of our method to diverse geomet-
‘flower’ examples, our method has much less space left, and the dis-
                                                                                 ric configurations.
tribution is more even. Our method outperformed ShapeImage in all
                                                                                    The Curse of Local Minima. Like any other iterative optimization
three metrics. As can be seen in the ‘Moon’ and ‘Fish’ examples, our
                                                                                 algorithms with loss functions, our method can get stuck in some
method achieves larger coverage, but with much more even distribu-
                                                                                 local minima, when visual primitives are not well-fitted in the target
tion, less overlap among objects, and less exceeding from the target
                                                                                 shape. When some small primitives are fully contained in some big
shapes. As shown in the ‘Australia’ and ‘Letter P’ examples, PAD gets
                                                                                 elements, they are shadow-trapped. This obstruction leads to a state of
a more compact layout than ours, with less space left, which results in
                                                                                 stagnation, where the primitive remains stationary and unable to move.
better scores in Layout Coverage. However, PAD causes more severe
                                                                                 Some techniques can be used to alleviate the curse of local minima. For
overlapping (i.e., the red and blue areas in Figure 12) than ours.
                                                                                 example, a sheepherder algorithm can be integrated into the collage
                                                                                 optimization procedure, which can monitor and report problems in a
7 Conclusion and Future Work                                                     global scope, such as detecting the coverage of visual elements, etc.
In this work, we have introduced a neat approach to creating collage                Hybrid Object- and Image-space In Figure 12, we demonstrate that
and packing visualizations by leveraging vector graphics manipulation our method outperforms other object-based approaches in collage gen-
through an optimization process aimed at minimizing loss in image eration, especially in terms of compactness and non-overlap. However,
space. Through the diverse examples presented in Section 5, we have object-space methods have distinct advantages. For instance, methods
demonstrated the versatility of our method in generating visually com- like Minkowski Penalty [28] provide finer control over object proper-
pelling collages. Compared to object-based methods such as PAD [18] ties, such as preserving balance and harmony among selected objects.
and Minkowski Penalty [28], our method offers the advantages of A promising future direction would be to incorporate object-space loss
being free from object-specific representations and achieving greater into our framework to refine spatial relationships further and enhance
computational scalability. Our image-space approach empowers users layout quality.
to explore their creativity, experiment with novel visual elements, and

                                                                                                         SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
8 •    Zhenyu Wang and Min Lu


Acknowledgments                                                                             [21] Chenlu Li, Xiaoju Dong, and Xiaoru Yuan. 2018. Metro-wordle: An interactive
                                                                                                 visualization for urban text distributions based on wordle. Visual Informatics 2, 1
We are deeply grateful to Prof. Daniel Cohen-Or and Prof. Dani Lischin-      (2018), 50–59.
ski for their encouragement and insightful feedback throughout this [22] Tzu-Mao Li, Michal Lukáč, Michaël Gharbi, and Jonathan Ragan-Kelley. 2020. Differ-
                                                                             entiable vector graphics rasterization for editing and learning. ACM Transactions on
work. We also thank the anonymous reviewers for their constructive           Graphics (TOG) 39, 6 (2020), 1–15.
suggestions. This work is supported in parts by fundings from Shen- [23] Lingjie Liu, Hongjie Zhang, Guangmei Jing, Yanwen Guo, Zhonggui Chen, and
zhen Science and Technology Program (20231122121504001), National            Wenping Wang. 2017. Correlation-preserving photo collage. IEEE transactions on
                                                                             visualization and computer graphics 24, 6 (2017), 1956–1968.
Natural Science Foundation of China (NSFC) Program (62472288), and [24] Shixia Liu, Jialun Yin, Xiting Wang, Weiwei Cui, Kelei Cao, and Jian Pei. 2015. Online
Guangdong Laboratory of Artificial Intelligence and Digital Economy          visual analytics of text streams. IEEE transactions on visualization and computer
(SZ), MNR Key Laboratory for Geo-Environmental Monitoring of Great           graphics 22, 11 (2015), 2451–2466.
                                                                        [25] Y. Ma, Z. Chen, W. Hu, and W. Wang. 2018. Packing Irregular Objects in 3D Space via
Bay Area, and Guangdong Key Laboratory of Urban Informatics.                 Hybrid Optimization. Computer Graphics Forum 37, 5 (2018), 49–59. https://doi.org/
                                                                                                 10.1111/cgf.13490 arXiv:https://onlinelibrary.wiley.com/doi/pdf/10.1111/cgf.13490
                                                                                            [26] Ron Maharik, Mikhail Bessmeltsev, Alla Sheffer, Ariel Shamir, and Nathan Carr. 2011.
References                                                                                       Digital micrography. ACM Transactions on Graphics (TOG) 30, 4 (2011), 1–12.
                                                                                            [27] Carmel McNaught and Paul Lam. 2010. Using Wordle as a supplementary research
 [1] Ming-Te Chi, Shih-Syun Lin, Shiang-Yi Chen, Chao-Hung Lin, and Tong-Yee Lee. 2015.          tool. Qualitative Report 15, 3 (2010), 630–643.
     Morphable word clouds for time-varying text data visualization. IEEE transactions on [28] Jiří Minarčík, Sam Estep, Wode Ni, and Keenan Crane. 2024. Minkowski penalties:
     visualization and computer graphics 21, 12 (2015), 1415–1426.                               Robust differentiable constraint enforcement for vector graphics. In ACM SIGGRAPH
 [2] Weiwei Cui, Yingcai Wu, Shixia Liu, Furu Wei, Michelle X Zhou, and Huamin Qu.               2024 Conference Papers. 1–12.
     2010. Context preserving dynamic word cloud visualization. In 2010 IEEE Pacific [29] Reiichiro Nakano. 2019. Neural painters: A learned differentiable constraint for
     Visualization Symposium (PacificVis). IEEE, 121–128.                                        generating brushstroke paintings. arXiv preprint arXiv:1904.08410 (2019).
 [3] Ketan Dalal, Allison W. Klein, Yunjun Liu, and Kaleigh Smith. 2006. A spectral [30] Xingjia Pan, Fan Tang, Weiming Dong, Chongyang Ma, Yiping Meng, Feiyue Huang,
     approach to NPR packing. In Proceedings of the 4th International Symposium on Non-          Tong-Yee Lee, and Changsheng Xu. 2019. Content-based visual summarization for
     Photorealistic Animation and Rendering (Annecy, France) (NPAR ’06). Association for         image collections. IEEE transactions on visualization and computer graphics 27, 4
     Computing Machinery, New York, NY, USA, 71–78. https://doi.org/10.1145/1124728.             (2019), 2298–2312.
     1124741                                                                                [31] Deokgun Park, Steven M Drucker, Roland Fernandez, and Niklas Elmqvist. 2017.
 [4] Daniel Dorling. 2011. Area Cartograms: Their Use and Creation. Vol. 59. 252 – 260.          Atom: A grammar for unit visualizations. IEEE transactions on visualization and
 [5] Stas Goferman, Ayellet Tal, and Lihi Zelnik-Manor. 2010. Puzzle-like collage. In            computer graphics 24, 12 (2017), 3032–3043.
     Computer graphics forum, Vol. 29. Wiley Online Library, 459–468.                       [32] Fernando V Paulovich, Franklina MB Toledo, Guilherme P Telles, Rosane Minghim,
 [6] Yuqi Gong, Xuehui Yu, Yao Ding, Xiaoke Peng, Jian Zhao, and Zhenjun Han.                    and Luis Gustavo Nonato. 2012. Semantic wordification of document collections. In
     2021. Effective Fusion Factor in FPN for Tiny Object Detection. In 2021 IEEE                Computer Graphics Forum, Vol. 31. Wiley Online Library, 1145–1153.
     Winter Conference on Applications of Computer Vision (WACV). 1159–1167. https: [33] Andrew Ramsden and Andrew Bate. 2008. Using word clouds in teaching and learning.
     //doi.org/10.1109/WACV48630.2021.00120                                                      (2008).
 [7] Marti A Hearst, Emily Pedersen, Lekha Patil, Elsie Lee, Paul Laskowski, and Steven [34] Bernhard Reinert, Tobias Ritschel, and Hans-Peter Seidel. 2013. Interactive by-
     Franconeri. 2019. An evaluation of semantically grouped word cloud designs. IEEE            example design of artistic packing layouts. ACM Transactions on Graphics (TOG) 32,
     transactions on visualization and computer graphics 26, 9 (2019), 2748–2761.                6 (2013), 1–7.
 [8] Stefan Hiller, Heino Hellwig, and Oliver Deussen. 2003. Beyond Stippling- [35] Anna W Rivadeneira, Daniel M Gruen, Michael J Muller, and David R Millen. 2007.
     Methods for Distributing Objects on the Plane.                   Computer Graphics          Getting our head in the clouds: toward evaluation studies of tagclouds. In Proceedings
     Forum 22, 3 (2003), 515–522.                 https://doi.org/10.1111/1467-8659.00699        of the SIGCHI conference on Human factors in computing systems. 995–998.
     arXiv:https://onlinelibrary.wiley.com/doi/pdf/10.1111/1467-8659.00699                  [36] Carsten Rother, Lucas Bordeaux, Youssef Hamadi, and Andrew Blake. 2006. Autocol-
 [9] Chen-Yuan Hsu, Li-Yi Wei, Lihua You, and Jian Jun Zhang. 2020. Autocomplete ele-            lage. ACM transactions on graphics (TOG) 25, 3 (2006), 847–852.
     ment fields. In Proceedings of the 2020 CHI Conference on Human Factors in Computing [37] Reza Adhitya Saputra, Craig S Kaplan, and Paul Asente. 2019. Improved deformation-
     Systems. 1–13.                                                                              driven element packing with repulsionpak. IEEE transactions on visualization and
[10] Wenchao Hu, Zhonggui Chen, Hao Pan, Yizhou Yu, Eitan Grinspun, and Wenping                  computer graphics 27, 4 (2019), 2396–2408.
     Wang. 2016. Surface Mosaic Synthesis with Irregular Tiles. IEEE Transactions on [38] ShapeCollage. [n. d.]. ShapeCollage. http://www.shapecollage.com/. Accessed:
     Visualization and Computer Graphics 22, 3 (2016), 1302–1313. https://doi.org/10.1109/       2024-07-08.
     TVCG.2015.2498620                                                                      [39] Yvonne Spielmann. 1999. Aesthetic features in digital imaging: collage and morph.
[11] Hua Huang, Lei Zhang, and Hong-Chao Zhang. 2011. Arcimboldo-like collage using              Wide Angle 21, 1 (1999), 131–148.
     internet images. In Proceedings of the 2011 SIGGRAPH Asia Conference. 1–8.             [40] Tatiana Surazhsky and Gershon Elber. 2002. Artistic surface rendering using layout
[12] Shir Iluz, Yael Vinker, Amir Hertz, Daniel Berio, Daniel Cohen-Or, and Ariel Shamir.        of text. In Computer Graphics Forum, Vol. 21. Wiley Online Library, 99–110.
     2023. Word-as-image for semantic typography. ACM Transactions on Graphics (TOG) [41] Oliver Van Kaick, Hao Zhang, Ghassan Hamarneh, and Daniel Cohen-Or. 2011. A
     42, 4 (2023), 1–11.                                                                         survey on shape correspondence. In Computer graphics forum, Vol. 30. Wiley Online
[13] Takayuki Itoh, Yumi Yamaguchi, Yuko Ikehata, and Yasumasa Kajinaga. 2004. Hierar-           Library, 1681–1707.
     chical data visualization using a fast rectangle-packing algorithm. IEEE Transactions [42] Fernanda B Viegas, Martin Wattenberg, and Jonathan Feinberg. 2009. Participatory
     on Visualization and Computer Graphics 10, 3 (2004), 302–313.                               visualization with wordle. IEEE transactions on visualization and computer graphics
[14] Ajay Jain, Amber Xie, and Pieter Abbeel. 2023. Vectorfusion: Text-to-svg by ab-             15, 6 (2009), 1137–1144.
     stracting pixel-based diffusion models. In Proceedings of the IEEE/CVF Conference on [43] Roel Vliegen, Jarke J Van Wijk, and Erik-Jan van der Linden. 2006. Visualizing
     Computer Vision and Pattern Recognition. 1911–1920.                                         business data with generalized treemaps. IEEE Transactions on visualization and
[15] Jaemin Jo, Bongshin Lee, and Jinwook Seo. 2015. WordlePlus: expanding wordle’s use          computer graphics 12, 5 (2006), 789–796.
     through natural interaction and animation. IEEE computer graphics and applications [44] Jingdong Wang, Long Quan, Jian Sun, Xiaoou Tang, and Heung-Yeung Shum. 2006.
     35, 6 (2015), 20–28.                                                                        Picture collage. In 2006 IEEE Computer Society Conference on Computer Vision and
[16] Junhwan Kim, Fabio Pellacini, et al. 2002. Jigsaw image mosaics. ACM Transactions           Pattern Recognition (CVPR’06), Vol. 1. IEEE, 347–354.
     on Graphics 21, 3 (2002), 657–664.                                                     [45] Weixin Wang, Hui Wang, Guozhong Dai, and Hongan Wang. 2006. Visualization of
[17] Kyle Koh, Bongshin Lee, Bohyoung Kim, and Jinwook Seo. 2010. Maniwordle: Pro-               large hierarchical data by circle packing. In Proceedings of the SIGCHI conference on
     viding flexible control over wordle. IEEE Transactions on Visualization and Computer        Human Factors in computing systems. 517–520.
     Graphics 16, 6 (2010), 1190–1197.                                                      [46] Yunhai Wang, Xiaowei Chu, Kaiyi Zhang, Chen Bao, Xiaotong Li, Jian Zhang, Chi-
[18] Kin Chung Kwan, Lok Tsun Sinn, Chu Han, Tien-Tsin Wong, and Chi-Wing Fu. 2016.              Wing Fu, Christophe Hurter, Oliver Deussen, and Bongshin Lee. 2019. Shapewordle:
     Pyramid of arclength descriptor for generating collage of shapes. ACM Trans. Graph.         tailoring wordles using shape-aware archimedean spirals. IEEE Transactions on
     35, 6 (2016), 229–1.                                                                        Visualization and Computer Graphics 26, 1 (2019), 991–1000.
[19] Der-Tsai Lee. 1982. Medial axis transformation of a planar shape. IEEE Transactions [47] Yingcai Wu, Thomas Provan, Furu Wei, Shixia Liu, and Kwan-Liu Ma. 2011. Semantic-
     on pattern analysis and machine intelligence 4 (1982), 363–369.                             preserving word clouds by seam carving. In Computer Graphics Forum, Vol. 30. Wiley
[20] Ganghun Lee, Minji Kim, Yunsu Lee, Minsu Lee, and Byoung-Tak Zhang. 2023. Neural            Online Library, 741–750.
     collage transfer: Artistic reconstruction via material manipulation. In Proceedings of
     the IEEE/CVF International Conference on Computer Vision. 2394–2405.


SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
                                                                                                  Image-Space Collage and Packing with Differentiable Rendering   • 9


[48] Gerhard Wäscher, Heike Haußner, and Holger Schumann. 2007. An improved typol-
     ogy of cutting and packing problems. European Journal of Operational Research 183,
     3 (2007), 1109–1130. https://doi.org/10.1016/j.ejor.2005.12.047
[49] Liwenhan Xie, Xinhuan Shu, Jeon Cheol Su, Yun Wang, Siming Chen, and Huamin
     Qu. 2023. Creating emordle: Animating word cloud for emotion expression. IEEE
     Transactions on Visualization and Computer Graphics (2023).
[50] Jie Xu and Craig S Kaplan. 2007. Calligraphic packing. In Proceedings of Graphics
     Interface 2007. 43–50.
[51] Xuemiao Xu, Linling Zhang, and Tien-Tsin Wong. 2010. Structure-based ASCII art.
     In ACM SIGGRAPH 2010 papers. 1–10.
[52] Junsong Zhang, Zuyi Yang, Linchengyu Jin, Zhitang Lu, and Jinhui Yu. 2022. Creating
     Word Paintings Jointly Considering Semantics, Attention, and Aesthetics. ACM
     Transactions on Applied Perceptions (TAP) 19, 3 (2022), 1–21.
[53] Jian Zhao, Nan Cao, Zhen Wen, Yale Song, Yu-Ru Lin, and Christopher Collins. 2014.
     # FluxFlow: Visual analysis of anomalous information spreading on social media.
     IEEE transactions on visualization and computer graphics 20, 12 (2014), 1773–1782.
[54] Ningyuan Zheng, Yifan Jiang, and Dingjiang Huang. 2018. Strokenet: A neural
     painting environment. In International Conference on Learning Representations.
[55] Qiubing Zhuang, Zhonggui Chen, Keyu He, Juan Cao, and Wenping Wang. 2024.
     Dynamics simulation-based packing of irregular 3D objects. Computers & Graphics
     123 (2024), 103996. https://doi.org/10.1016/j.cag.2024.103996
[56] Changqing Zou, Junjie Cao, Warunika Ranaweera, Ibraheem Alhashim, Ping Tan,
     Alla Sheffer, and Hao Zhang. 2016. Legible compact calligrams. ACM Transactions on
     Graphics (TOG) 35, 4 (2016), 1–12.




                                                                                           SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
10   •   Zhenyu Wang and Min Lu




 Fig. 13. A gallery of examples: diverse visual elements (i.e., icons, sketched paths) can be effectively fitted within convex and concave target boundaries.




SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
                                                                     Image-Space Collage and Packing with Differentiable Rendering   •   11




Fig. 14. A gallery of examples that texts and graphics are collaged and packed for visually appealing design.



                                                               SIGGRAPH Conference Papers’ 25, August 10-14, 2025, Vancouver, BC, Canada.
