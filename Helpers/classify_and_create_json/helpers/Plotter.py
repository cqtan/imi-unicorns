import matplotlib.pyplot as plt
import numpy as np
import keras

# plot the training loss and accuracy
class TrainPlotter:
    def __init__(self, history, epochs, file_postfix):
        self.history = history
        self.epochs = epochs
        self.file_postfix = file_postfix

    def PlotLossAndAcc(self):
        plt.style.use("ggplot")
        plt.figure()
        N = self.epochs
        plt.plot(np.arange(0, N), self.history.history["loss"], label="train_loss")
        plt.plot(np.arange(0, N), self.history.history["val_loss"], label="val_loss")
        plt.plot(np.arange(0, N), self.history.history["acc"], label="train_acc")
        plt.plot(np.arange(0, N), self.history.history["val_acc"], label="val_acc")
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="upper left")
        plt.savefig("plot-" + self.file_postfix)
        
