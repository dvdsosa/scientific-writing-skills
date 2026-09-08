Hardware acceleration cuts inference latency for convolutional neural networks on
resource-constrained embedded platforms, but quantising the weights to eight-bit
integers costs detection accuracy, and memory pressure climbs sharply once the
batch size passes four.

Our pipeline pairs a lightweight backbone with hardware-accelerated non-maximum
suppression on the programmable logic of the Kria KV260, reaching 31 frames per
second at 1080p. The deep-learning processing unit talks to the programmable
logic over AXI4, and the processing system runs a PetaLinux image whose runtime
moves data between DDR and block RAM. These results match those reported for
comparable architectures, and the overhead stays under 3%. We chose this design
because most published solutions rely on it.
