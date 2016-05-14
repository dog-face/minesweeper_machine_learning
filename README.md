# minesweeper_machine_learning
Minesweeper solver trained using machine learning

Requires numpy and sklearn to run

Pre-generated training data has been saved to disk via pickle, and can be found in the data/ folder. <br/>
If you wish to generate fresh training data:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;for the generation method of learning:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;run `fivexfive_svm/fivexfive_block_generator.py`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;for the gameplay method of learning:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;there are some lines in `fivexfive_svm/fivexfive_svm_tester.py` that need to be uncommented. These lines can be found by searching for "#Generate data as we go"<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;then run the `fivexfive_svm_tester.py` until you are satisfied with the quantity of data generated.

If you're satisfied with the existing training data, and simply want to train the classifiers:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;`fivexfive_svm/generation_svm_trainer.py` will train the generation classifier<br/>
&nbsp;&nbsp;&nbsp;&nbsp;`fivexfive_svm/gameplay_svm_trainer.py` will train the gameplay classifier.

The generation classifier is trained on randomly generated data.<br/>
The gameplay classifier is trained on data from real games the computer has already played. In theory, it should improve with each iteration of train -> generate new data -> train -> etc.

To see actual gameplay, use `fivexfive_svm/fivexfive_svm_tester.py`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;To change which classifier is tested, change the line commented "`#choose your classifier here`"

To view some statistics, run `report_data/combined_validation.py`

To see some baseline algorithms play, run the files in `baseline_algorithms/`

To play a game yourself, uncomment the last line in `emulator/minesweeper_emulator.py` and run it. 

