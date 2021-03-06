import subprocess
import numpy as np
import pandas as pd
from preprocess_dataset import symbol_to_one_hot, N_ELS

# noinspection SpellCheckingInspection
MAPPING_CSV_FILE_NAME = "dataset/ogbg_molhiv/mapping/mol.csv"
N_COORDINATES = 3


class Smiles2Coord:

    @staticmethod
    def __get_file_name_from_index(index: int):
        # noinspection SpellCheckingInspection
        # proc = subprocess.Popen(
        #     f'ls -- dataset/coordinate-files/{index}-*.npy', stdout=subprocess.PIPE, shell=True
        # )
        # tmp = proc.stdout.read().decode("utf-8").strip()
        # return tmp
        return f"dataset/coordinate-files/{index}.npy"

    @staticmethod
    def __get_file_name_from_smiles_string(index: int, smiles_string: str):
        # noinspection SpellCheckingInspection
        # return f"dataset/coordinate-files/{index}-{smiles_string}.npy"
        # noinspection SpellCheckingInspection
        return f"dataset/coordinate-files/{index}.npy"

    @staticmethod
    def read_coord_from_file(item_index: int):
        file_name = Smiles2Coord.__get_file_name_from_index(item_index)
        molecule_readout = np.load(file_name, allow_pickle=True)
        # for coord in molecule_readout:
        #     print(coord)
        # print(molecule_readout)
        return molecule_readout

    @staticmethod
    def smiles2coord(smiles_string: str, index: int, verbose: bool = False):
        """
        Must have open-babel installed (e.g. brew install open-babel)
        :param smiles_string:
        :param index:
        :param verbose:
        :return:
        """
        # noinspection SpellCheckingInspection
        proc = subprocess.Popen(
            f'obabel -:"{smiles_string}" -oxyz -h --gen3D -c', stdout=subprocess.PIPE, shell=True
        )
        tmp = proc.stdout.read()
        molecule_readout = np.array(tmp.decode("utf-8").split('\n')[2:-1])
        if verbose:
            print(len(molecule_readout))
            for item in molecule_readout:
                print(item)
            print(molecule_readout)
            print("------")

        # Convert strings in data to 2d array
        def get_split(x):
            return np.array(x.split(), dtype=object)

        out = np.zeros((molecule_readout.size, N_COORDINATES + N_ELS), dtype=object)

        elements = list()
        for i, coord in enumerate(molecule_readout):
            item_split = get_split(coord)
            out[i, -N_COORDINATES:] = item_split[1:]
            elements.append(item_split[0])

        coordinates = out
        # print(coordinates[:, -N_COORDINATES:])
        coordinates[:, -N_COORDINATES:] = coordinates[:, -N_COORDINATES:].astype('float64')

        # Separate elements from coordinates
        elements = symbol_to_one_hot(elements)
        coordinates[:, :N_ELS] = elements

        if verbose:
            print(coordinates)

        np.save(Smiles2Coord.__get_file_name_from_smiles_string(index, smiles_string), coordinates)


if __name__ == '__main__':
    # check 22269
    # 36055
    smiles_strings = pd.read_csv(MAPPING_CSV_FILE_NAME)['smiles']
    index_count = 0
    for smile_string in smiles_strings:
        if index_count < 22268:
            index_count += 1
            continue
        print(index_count, smile_string)
        Smiles2Coord.smiles2coord(smile_string, index_count, verbose=False)
        Smiles2Coord.read_coord_from_file(index_count)
        index_count += 1
