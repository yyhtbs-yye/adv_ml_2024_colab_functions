import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def save_grid_images(inps, name_dict, labels, predicted, nrow=8, show_only_incorrect=False):
    if show_only_incorrect:
        # Filter to include only incorrect predictions
        incorrect_indices = [i for i, (l, p) in enumerate(zip(labels, predicted)) if l != p]
        inps = inps[incorrect_indices]
        labels = [labels[i] for i in incorrect_indices]
        predicted = [predicted[i] for i in incorrect_indices]
        
    titles = [f'T:{name_dict[l]}/P:{name_dict[p]}' for l, p in zip(labels, predicted)]
    n_images = inps.shape[0]
    ncol = int(np.ceil(n_images / nrow))
    
    fig = make_subplots(rows=ncol, cols=nrow, subplot_titles=titles)
    
    img_idx = 0
    for r in range(1, ncol + 1):
        for c in range(1, nrow + 1):
            if img_idx < n_images:
                fig.add_trace(go.Image(z=inps[img_idx]), row=r, col=c)
            img_idx += 1
    
    # Update layout to hide axis ticks and labels
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    
    # Adjust margins to fit titles and ensure layout is tight
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
    
    # Save figure to a PNG file
    fig.write_image("grid_figure.png")
