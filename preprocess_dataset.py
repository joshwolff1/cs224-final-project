from mendeleev import element
import numpy as np

N_ELS = 118
ELEMENTS = [
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
    'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
    'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y',
    'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
    'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba',
    'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd',
    'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf',
    'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
    'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra',
    'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk',
    'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg',
    'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc',
    'Lv', 'Ts', 'Og'
]


def symbol_to_one_hot(symbols):
    eltonum = lambda x : element(str(x)).atomic_number - 1
    symbols = map(eltonum, symbols)
    symbols = list(symbols)
    symbol_len = len(symbols)
    symbols_one_hot = np.zeros((symbol_len, N_ELS))
    symbols_one_hot[np.arange(symbol_len), symbols] = 1
    return symbols_one_hot


if __name__ == '__main__':

    # elem_to_one_hot_dict = dict()
    # for elem in ELEMENTS:
    #     elem_to_one_hot_dict[elem] = symbol_to_one_hot([elem])[0]
    #
    # print(elem_to_one_hot_dict)
    # np.save("elem_to_one_hot_dict.npy", elem_to_one_hot_dict)

    print(np.load("elem_to_one_hot_dict.npy", allow_pickle=True))
    # print(len(set(ELEMENTS)))
    #
    # eltonum = lambda x: element(str(x)).atomic_number
    # print(eltonum('Li'))
    # for item in map(eltonum, ['Be', 'Li']):
    #     print(item)
    # print(symbol_to_one_hot(['Be', 'Li']))
