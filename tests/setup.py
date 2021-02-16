def prepare_test_file():
    raw_data = ["######\n",
                "  ##  \n",
                "#    #\n",
                "# ## #\n",
                "#    #\n",
                "######\n"]
    with open("test_file.txt", "w+") as test_file:
        test_file.writelines(raw_data)
