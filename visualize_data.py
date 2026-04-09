import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# Read CSV data
df = pd.read_csv('logs/data.csv')

# Normalize column names if needed
if 'speed' in df.columns and 'download_speed_mbps' not in df.columns:
    df = df.rename(columns={'speed': 'download_speed_mbps'})

# Convert timestamp to datetime for better plotting
if 'timestamp' in df.columns:
    df['datetime'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S', errors='coerce')
else:
    raise ValueError('logs/data.csv must contain a timestamp column')

# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Download Speed Over Time (All Clients)
ax1 = axes[0, 0]
for client in df['client_id'].unique():
    client_data = df[df['client_id'] == client]
    ax1.plot(range(len(client_data)), client_data['download_speed_mbps'], 
             marker='o', label=client, linewidth=2, markersize=5)
ax1.set_xlabel('Data Point Index', fontsize=11)
ax1.set_ylabel('Download Speed (Mbps)', fontsize=11)
ax1.set_title('Download Speed Over Time (All Clients)', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Speed Distribution by Client (Box Plot)
ax2 = axes[0, 1]
df.boxplot(column='download_speed_mbps', by='client_id', ax=ax2)
ax2.set_xlabel('Client ID', fontsize=11)
ax2.set_ylabel('Download Speed (Mbps)', fontsize=11)
ax2.set_title('Download Speed Distribution by Client', fontsize=12, fontweight='bold')
plt.sca(ax2)
plt.xticks(rotation=0)

# 3. Average Speed by Client (Bar Chart)
ax3 = axes[1, 0]
avg_speed = df.groupby('client_id')['download_speed_mbps'].mean()
bars = ax3.bar(avg_speed.index, avg_speed.values, color=['#1f77b4', '#ff7f0e'], alpha=0.7)
ax3.set_xlabel('Client ID', fontsize=11)
ax3.set_ylabel('Average Download Speed (Mbps)', fontsize=11)
ax3.set_title('Average Download Speed by Client', fontsize=12, fontweight='bold')
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.3f}', ha='center', va='bottom', fontsize=10)
ax3.grid(True, alpha=0.3, axis='y')

# 4. Statistics Summary (Text)
ax4 = axes[1, 1]
ax4.axis('off')
stats_text = f"""
NETWORK ANALYSIS STATISTICS

Total Data Points: {len(df)}
Unique Clients: {df['client_id'].nunique()}

Overall Statistics:
  • Min Speed: {df['download_speed_mbps'].min():.4f} Mbps
  • Max Speed: {df['download_speed_mbps'].max():.4f} Mbps
  • Mean Speed: {df['download_speed_mbps'].mean():.4f} Mbps
  • Std Dev: {df['download_speed_mbps'].std():.4f} Mbps

Per Client:
"""

for client in sorted(df['client_id'].unique()):
    client_stats = df[df['client_id'] == client]['download_speed_mbps']
    stats_text += f"\n  {client}:"
    stats_text += f"\n    - Avg: {client_stats.mean():.4f} Mbps"
    stats_text += f"\n    - Min: {client_stats.min():.4f} Mbps"
    stats_text += f"\n    - Max: {client_stats.max():.4f} Mbps"

ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=10,
        verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('logs/network_analysis_graph.png', dpi=300, bbox_inches='tight')
print("✓ Graph saved to 'logs/network_analysis_graph.png'")
plt.show()
