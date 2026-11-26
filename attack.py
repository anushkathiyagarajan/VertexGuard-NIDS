import matplotlib.pyplot as plt
import numpy as np

# Professional style
plt.style.use('seaborn-v0_8')

# Attack classes
attack_classes = ['N', 'G', 'F', 'E', 'R', 'D']

# Base paper recall values
federated_ids = [94, 97, 85, 21, 57, 74]

# Your project recall values
vertexguard_ids = [98, 99, 96, 80, 92, 95]

x = np.arange(len(attack_classes))

plt.figure(figsize=(10,6))

# Base paper line
plt.plot(x, federated_ids,
         marker='o',
         linewidth=3,
         markersize=8,
         label='Federated IDS',
         color='#00CED1')

# Your project line
plt.plot(x, vertexguard_ids,
         marker='o',
         linewidth=3,
         markersize=8,
         label='VertexGuard IDS',
         color='#4B3F99')

plt.title("Attack Class Detection Comparison", fontsize=16, fontweight='bold')
plt.xlabel("Attack Classes", fontsize=12)
plt.ylabel("Recall (%)", fontsize=12)

plt.xticks(x, attack_classes, fontsize=11)
plt.yticks(fontsize=11)

plt.ylim(0,100)

plt.grid(True, linestyle='--', alpha=0.6)

plt.legend(loc='lower right', fontsize=12)

# Add percentage labels
for i, value in enumerate(federated_ids):
    plt.text(i, value + 1, f'{value}%', ha='center', fontsize=10)

for i, value in enumerate(vertexguard_ids):
    plt.text(i, value + 1, f'{value}%', ha='center', fontsize=10)

plt.tight_layout()

# Save high quality image
plt.savefig("attack_class_line_comparison.png", dpi=300)

plt.show()