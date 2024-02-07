import torch 

def get_labels_and_predictions(model, dataloader, to_cpu=True):
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
                # X = X.cpu()
                y = y.cpu()
                y_hat = y_hat.cpu()

    return y, y_hat
