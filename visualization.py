# visualization.py
# Matplotlib visualizations - bar chart and radar chart

import matplotlib.pyplot as plt
import numpy as np

def create_bar_chart(interest_vector, output_path="interest_bar.png"):
    """
    Create bar chart of interest distribution.
    """
    # Sort by value
    sorted_items = sorted(interest_vector.items(), key=lambda x: x[1], reverse=True)
    categories = [item[0] for item in sorted_items[:10]]  # Top 10
    values = [item[1] for item in sorted_items[:10]]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(categories, values, color='steelblue', alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=9)
    
    plt.xlabel('Category', fontsize=12, fontweight='bold')
    plt.ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    plt.title('Interest Distribution (Top 10 Categories)', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  ✓ Bar chart saved: {output_path}")
    plt.close()


def create_radar_chart(interest_vector, output_path="interest_radar.png"):
    """
    Create radar chart of interest distribution.
    """
    # Get top 8 categories for radar (more than 8 becomes cluttered)
    sorted_items = sorted(interest_vector.items(), key=lambda x: x[1], reverse=True)
    categories = [item[0] for item in sorted_items[:8]]
    values = [item[1] for item in sorted_items[:8]]
    
    # Number of variables
    num_vars = len(categories)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Close the plot
    values += values[:1]
    angles += angles[:1]
    categories += categories[:1]
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Draw the plot
    ax.plot(angles, values, 'o-', linewidth=2, color='steelblue', label='Interest Level')
    ax.fill(angles, values, alpha=0.25, color='steelblue')
    
    # Fix axis to go in the right order
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw axis lines for each angle and label
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories[:-1], fontsize=11)
    
    # Set y-axis limits
    ax.set_ylim(0, max(values) * 1.1)
    
    # Add title
    plt.title('Interest Distribution Radar', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  ✓ Radar chart saved: {output_path}")
    plt.close()


def create_all_visualizations(interest_vector):
    """
    Generate all visualization outputs.
    """
    print("📈 Creating visualizations...")
    
    create_bar_chart(interest_vector)
    create_radar_chart(interest_vector)
    
    print("✅ Visualizations complete\n")
