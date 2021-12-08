----------------------------------------
       Python Sample 테스트 방법
----------------------------------------
1. Lifecycle 테스트
 1) lifecycle 폴더 안에 있는 ipynb 파일들로 테스트 가능합니다. 각 파일은 데이터와 분석 방법이 다르게 구성되어 있습니다.
    파일을 위에서부터 순차적으로 실행시킵니다.

 2) 실행 결과가 experiment 리스트에 보여집니다. 생성된 experiment를 배포 저장소에 저장합니다.
    파일 내용을 모두 수행하면, 모델 학습-저장이 모두 완료된 상태 입니다.

 3) 배포 저장소 상세 페이지에서, runs/best-model 아래에 있는 모델 파일을 체크하고, 이름을 저장해 둡니다.
    DL 모델링 h5, json 파일, ML 모델은 joblib 파일입니다.

 4) 배포 저장소의 api 코드에 deploy 폴더 안에 있는 py 파일 내용을 붙여넣습니다. 데이터와 분석 방법에 맞는 flask 코드가 준비되어 있습니다.
    DL 모델의 경우
        json_file = open('json_file_name', 'r', opener=opener)  # json_file_name 수정
        loaded_model.load_weights('runs/best-model/h5_file_name')  # h5_file_name 수정
    부분에,
    ML 모델의 경우
        loaded_model = joblib.load("./runs/best-model/joblib_file_name")  # edit joblib_file_name
    부분에 저장해 두었던 모델 파일 이름을 기입하여 수정합니다.

 5) 모델을 배포한 후 배포 pod가 running 상태가 되면, 테스트 Endpoint로 들어 갑니다.
    swagger 화면의 try it out 버튼을 누르면 swagger api 모양은 모델에 따라 다릅니다.

    DL 모델의 경우, 파일을 업로드합니다.
        test_data와 test_label 파일을 업로드 합니다. 파일은 deploy/dp-test 폴더에 있습니다.
    ML 모델의 경우, json array 형식으로 직접 입력합니다.
        {"input_data": []} 가 기본 템플릿이며, [] 안에 테스트 할 데이터를 입력합니다. 테스트 데이터는 여러 개를 동시에 입력할 수 있습니다.
        입력할 변수의 개수는 Iris 4개, Breast cancer 30개, Boston 13개 입니다.
        ex. Iris의 경우, {"input_data": [[20, 20, 20, 20], [30, 30 30, 30]]}

    Execute 버튼을 눌러 데이터 결과를 확인 할 수 있습니다.
 
2. 모델링 & 시각화 테스트
 1) Visualize-DL-Keras-Classification-Iris.ipynb, Visualize-ML-Linear-Regression-Cars.ipynb)
 1) 파일을 위에서 순차적으로 실행시켜며, 학습 상태 및 차트 출력 상태를 확인합니다.

3. HDFS, Hive 연결 테스트(외부 퍼블릭망 오픈 또는 내부 클러스터 존재 시)
 1) HDFS 연결 테스트 - PythonHDFS.py
 2) Hive 연결 테스트 - PythonHive.py

----------------------------------------
            AutoDL 테스트 방법
----------------------------------------
1. 샘플 코드에 사용되는 데이터를 filestorage 디렉토리에 위치시킵니다.
2. 1에 따라 코드 상의 데이터 경로를 수정합니다.
3. jupyter notebook에서 easydict를 사용해 입력 파라미터를 설정했던 부분을
   argparse를 사용해 입력 파라미터를 설정하도록 수정합니다.
4. Edit > Merge Selected Cells와 %%writefile 파이썬_파일명.py magic command를 사용해
   jupyter notebook 파일(.ipynb)을 파이썬 파일(.py)로 저장합니다.
