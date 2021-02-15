from torch_geometric.data import DataLoader
from ogb.graphproppred import PygGraphPropPredDataset

if __name__ == "__main__":
    # noinspection SpellCheckingInspection
    data_set = PygGraphPropPredDataset(name='ogbg-molhiv')

    print(data_set.data)

    split_idx = data_set.get_idx_split()
    train_loader = DataLoader(data_set[split_idx['train']], batch_size=32, shuffle=True)
    valid_loader = DataLoader(data_set[split_idx['valid']], batch_size=32, shuffle=False)
    test_loader = DataLoader(data_set[split_idx['test']], batch_size=32, shuffle=False)

    print(data_set[split_idx['train']][0].edge_attr)
    print(data_set[split_idx['train']][0].edge_index)
    print(data_set[split_idx['train']][0].x)
    print(data_set[split_idx['train']][0].y)
    inputs = next(iter(train_loader))
    for my_input in inputs:
        print(len(my_input[1]))
        break
