import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def save_grid_images(images, labels, predicted, name_dict, nrow=8, show_only_incorrect=False):
    if show_only_incorrect:
        incorrect_indices = [i for i, (l, p) in enumerate(zip(labels, predicted)) if l != p]
        images = images[incorrect_indices]
        labels = [labels[i] for i in incorrect_indices]
        predicted = [predicted[i] for i in incorrect_indices]
        
    titles = [f'T:{name_dict[l]}/P:{name_dict[p]}' for l, p in zip(labels, predicted)]
    n_images = images.shape[0]
    ncol = int(np.ceil(n_images / nrow))
    
    fig = make_subplots(rows=ncol, cols=nrow, subplot_titles=titles)
    
    img_idx = 0
    for r in range(1, ncol + 1):
        for c in range(1, nrow + 1):
            if img_idx < n_images:
                fig.add_trace(go.Image(z=images[img_idx]), row=r, col=c)
            img_idx += 1
    
    # Update layout to hide axis ticks and labels
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    
    # Base size for each subplot (image)
    base_width_per_image = 64  # pixels
    base_height_per_image = 64  # pixels

    # Calculate total figure width and height
    total_width = base_width_per_image * nrow
    total_height = base_height_per_image * ncol
    
    # Adjust for margins and spacing if necessary
    adjusted_width = total_width + 100  # Adjust based on actual needs
    adjusted_height = total_height + 100  # Adjust based on actual needs
    
    # Adjust margins to fit titles and ensure layout is tight
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=False,
        width=adjusted_width,
        height=adjusted_height
    )
    
    # Save figure to a PNG file
    fig.write_image("grid_figure.png")
