# use torch to build a rbfnet to fit 2-d points.
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import copy

class RBFNet(nn.Module):
    def __init__(self, n = 5):
        super(RBFNet, self).__init__()
        # the number of neurons in hidden layer.
        # we have only one hidden layer here.
        # of couse we could build a deeper network
        self.N = n
        self.linear0 = nn.Linear(1, self.N)
        self.linear1 = nn.Linear(self.N, 1)
        self.c = 1 / np.sqrt(2 * np.pi)
    def forward(self, x):
        x = self.linear0(x)
        x = torch.mul(torch.pow(x, 2), -0.5)
        x = torch.mul(torch.exp(x), self.c)
        x = self.linear1(x)
        return x
net = RBFNet(10)
max_epoch = 500
optimizer = optim.SGD(net.parameters(), lr = 0.01)
criterion = nn.MSELoss()

def train_model_one_epoch(points):

    optimizer.zero_grad()
    sum_loss = 0
    for p in points:    
        _input = torch.Tensor([p[0]])
        _target = torch.Tensor([p[1]])
        output = net(_input)
        loss = criterion(output, _target)
        loss.backward()
        sum_loss += loss.item()
    optimizer.step()
    return sum_loss
def train_model():
        # show the dynamic process of convergence
    for epoch in range(max_epoch):
        loss = train_model_one_epoch(points)
        if epoch % (int(max_epoch/10)) == 0:
            print("epoch:", epoch, "loss:", loss)
def onclick_put_points(event):
    ix, iy = event.xdata, event.ydata
    points.append([ix, iy])
    plt.scatter(ix, iy, color="r")
    plt.draw()

def draw_model(net, label, color="blue"):
    x_coor = np.linspace(-5, 5, 100) 
    y_coor = [ net(torch.Tensor([tmp_x])).item() for tmp_x in x_coor]
    return plt.plot(x_coor, y_coor, label=label, c=color)

if __name__ == "__main__":


    # interactively put points
    fig = plt.figure()
    points = []
    fig.canvas.mpl_connect('button_press_event', onclick_put_points)
    plt.xlim((-5, 5))
    plt.ylim((-2, 2))
    plt.show()


    # open interactive mode
    plt.ion()
    # draw trained points
    np_points = np.array(points)
    x = np_points[:,0]
    y = np_points[:,1]

    init_net = copy.deepcopy(net)
    for epoch in range(max_epoch):
        plt.cla()
        plt.xlim((-5, 5))
        plt.ylim((-2, 2))
        loss = train_model_one_epoch(points)
        if epoch % (int(max_epoch/10)) == 0:
            print("epoch:", epoch, "loss:", loss)
        if epoch % (int(max_epoch/100)) == 0:
            plt.scatter(x, y, color='red')
            draw_model(net, "training", "orange")
            plt.pause(0.1)
    plt.ioff()

    plt.scatter(x, y, color='red')
    draw_model(init_net, color="cyan", label="before training")
    draw_model(net, color="orange", label="after training")
    plt.legend()
    plt.show()
    