As it is well known, the implementation of a hardware acceleration strategy
provides a reduction in the inference latency of convolutional neural networks
that are deployed on resource-constrained embedded platforms. However, a
degradation of the detection accuracy is caused by the quantisation of the
network weights to eight-bit integers. Therefore, there is a significant increase
in memory pressure when the batch size is raised above four. Furthermore, the
results were not inconsistent with those reported for comparable architectures,
and the overhead was not significant. Moreover, the proposed pipeline for
real-time defect detection, which combines a lightweight backbone with a
hardware-accelerated non-maximum suppression stage running on the programmable
logic of the Kria KV260, achieves 31 frames per second at 1080p. The DPU IP was
integrated into the PL via AXI4, and the PS ran a PetaLinux image with the XRT
stack managing DMA transfers between DDR and BRAM. Due to the fact that a
majority of the successful solutions rely on this approach, we adopted it.
