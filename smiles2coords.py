import subprocess
import numpy as np
import pandas as pd

# noinspection SpellCheckingInspection
MAPPING_CSV_FILE_NAME = "dataset/ogbg_molhiv/mapping/mol.csv"


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
        molecule_readout = np.load(file_name)
        return molecule_readout

    @staticmethod
    def smiles2coord(smiles_string: str, index: int, verbose: bool=False):
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
        np.save(Smiles2Coord.__get_file_name_from_smiles_string(index, smiles_string), molecule_readout)


if __name__ == '__main__':
    smiles_strings = pd.read_csv(MAPPING_CSV_FILE_NAME)['smiles']
    index_count = 0
    for smile_string in smiles_strings:
        print(index_count, smile_string)
        Smiles2Coord.smiles2coord(smile_string, index_count)
        Smiles2Coord.read_coord_from_file(index_count)
        index_count += 1
