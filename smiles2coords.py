import subprocess
import numpy as np
import pandas as pd
from preprocess_dataset import symbol_to_one_hot, N_ELS
from smiles2graph import smiles2graph

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
        # proc = subprocess.Popen(
        #     f'obabel -:"{smiles_string}" -oxyz -h --gen3D -c', stdout=subprocess.PIPE, shell=True
        # )
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

        not_corrupted = len(molecule_readout) != 0
        # print(len(molecule_readout), not_corrupted)
        if not_corrupted:
            atoms = 0
            passed_the_last_hydrogens = False
            for i, coord in reversed(list(enumerate(molecule_readout))):
                item_split = get_split(coord)
                if item_split[0] != 'H' or passed_the_last_hydrogens:
                    passed_the_last_hydrogens = True
                    atoms += 1

            out = np.zeros((atoms, N_COORDINATES + N_ELS), dtype=object)

            elements = list()
            curr_atom = atoms - 1
            passed_the_last_hydrogens = False
            for i, coord in reversed(list(enumerate(molecule_readout))):
                item_split = get_split(coord)
                # print( item_split[0])
                if item_split[0] != 'H' or passed_the_last_hydrogens:
                    passed_the_last_hydrogens = True
                    out[curr_atom, -N_COORDINATES:] = item_split[1:]
                    elements.insert(0, item_split[0])
                    # print(elements)
                    curr_atom -= 1

            coordinates = out
            # print(coordinates[:, -N_COORDINATES:])
            coordinates[:, -N_COORDINATES:] = coordinates[:, -N_COORDINATES:].astype('float64')

            # Separate elements from coordinates
            elements = symbol_to_one_hot(elements)
            coordinates[:, :N_ELS] = elements

            if verbose:
                print(f"Lend coordinates: {coordinates.shape}")
                coords_to_print = coordinates.tolist()
                print(coordinates[:, -N_COORDINATES:])
                for coord_to_print in coords_to_print:
                    print(coord_to_print)
                # print(coordinates.tolist())
        else:
            # corrupted_smiles_strings += 1
            print("Corrupted...")
            coordinates = np.zeros((smiles2graph(smiles_string)['num_nodes'], N_COORDINATES + N_ELS), dtype=object)
        print(f"BABEL ATOMS = {coordinates.shape[0]}")
        assert smiles2graph(smiles_string)['num_nodes'] == coordinates.shape[0]

        np.save(Smiles2Coord.__get_file_name_from_smiles_string(index, smiles_string), coordinates)
        return not_corrupted


if __name__ == '__main__':
    # Smiles2Coord.smiles2coord('CCC1=[O+][Cu-3]2([O+]=C(CC)C1)[O+]=C(CC)CC(CC)=[O+]2', 0, verbose=True)
    # graph = smiles2graph('O1C=C[C@H]([C@H]1O2)c3c2cc(OC)c4c3OC(=O)C5=C4CCC(=O)5')
    # check 22269
    # 36055

    print(Smiles2Coord.read_coord_from_file(21360))

    corrupted_smiles_strings = 0
    corrupted_indices = list()

    smiles_strings = pd.read_csv(MAPPING_CSV_FILE_NAME)['smiles']
    n_smiles = len(smiles_strings)
    index_count = 0
    for smile_string in smiles_strings:
        if index_count < 21360:
            index_count += 1
            continue
        not_corrupted = Smiles2Coord.smiles2coord(smile_string, index_count, verbose=False)
        if not not_corrupted:
            corrupted_smiles_strings += 1
            corrupted_indices.append(index_count)
        print(index_count + 1, corrupted_smiles_strings, n_smiles, smile_string, corrupted_indices)
        Smiles2Coord.read_coord_from_file(index_count)
        index_count += 1
        # if index_count > 5239:
        #     break

    print(corrupted_indices)
