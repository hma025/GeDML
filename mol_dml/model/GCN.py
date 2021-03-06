import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.nn import global_mean_pool


class GCN(nn.Module):
    def __init__(self, num_node_feats, dim_out):
        super(GCN, self).__init__()
        self.gc1 = GCNConv(num_node_feats, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.gc2 = GCNConv(256, 256)
        self.bn2 = nn.BatchNorm1d(256)
        self.fc2 = nn.Linear(256, 196)
        self.bn3 = nn.BatchNorm1d(196)
        self.fc3 = nn.Linear(196, dim_out)

    def forward(self, g):
        h = F.relu(self.bn1(self.gc1(g.x, g.edge_index)))
        h = F.relu(self.bn2(self.gc2(h, g.edge_index)))
        hg = global_mean_pool(h, g.batch)
        h = F.relu(self.bn3(self.fc2(hg)))
        out = self.fc3(h)

        return out, hg
