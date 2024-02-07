import torch 

def get_all(model, dataloader, to_cpu=True):
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        correct = 0
        total = 0
        for X, y in dataloader:
            if torch.cuda.is_available():
                X, y = X.cuda(), y.cuda()
            y_hat = model(X)
            _, y_hat = torch.max(y_hat.data, 1)

            # Convert the batch of X and predictions to CPU for visualization
            if to_cpu:
                X = X.cpu()
                y = y.cpu()
                y_hat = y_hat.cpu()

    return X, y, y_hat

def unnormalize(images, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]):
    # The mean and std have to be reshaped to [C, 1, 1] to match the tensor dimensions.
    mean = torch.tensor(mean).view(1, -1, 1, 1)
    std = torch.tensor(std).view(1, -1, 1, 1)
    
    if images.is_cuda:
        mean = mean.cuda()
        std = std.cuda()
    
    images.mul_(std).add_(mean)  # This modifies the tensor in-place
    return images
