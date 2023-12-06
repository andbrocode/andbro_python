def __save_to_pickle(obj, path, name):

    import os
    import pickle

    ofile = open(path+name+".pkl", 'wb')
    pickle.dump(obj, ofile)

    if os.path.isfile(path+name+".pkl"):
        print(f"\n -> created:  {path}{name}.pkl")

