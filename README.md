# **rOS EdgeRunner**

## 오픈 소스 소개
> **rOS는 모든 하위 버전을 포함하여 오픈소스 프로젝트 입니다.** 이 말은 누구나 해당 코드를 참고 하거나 수정할 수 있다는 말입니다.
> 
> rOS를 어떤 방식으로든 사용할 경우 해당 **프로젝트에 대한 출처**를 명시하고 **rOS기반이란걸 표시**해야 합니다.
> 
> rOS는 기본적으로 모두에게 오픈소스 프로젝트이지만, **출처를 안남기고 사용하거나 비도덕적인 목적을 가지고 사용할 경우에 한하여는 클로즈드소스**이며, 본인이 수정한 코드는 모두 **devMaxTrauma. Inc.와 개발자가 소유권을 행사할 수 있습니다.**
> 
> **rOS를 어떤 방식으로든 사용할 경우 위 사항을 모두 동의하는 것으로 간주합니다.**

## rOS EdgeRunner 소개
rOS EdgeRunner는 이름에서 EdgeRunner를 보고 알 수 있듯, Ayaka, Bleach, Clannad, Demonslayer를 이은 5번째 메이저 버전의 rOS입니다.

다른 버전의 rOS도 git branch로 확인할 수 있습니다.

rOS는 모두 Python기반으로 작성되었으며 RaspberryPI OS와 **macOS**, Windows에서 모두 필요 라이브러리만 설치하면 사용할 수 있습니다.

rOS의 구성은 ROS.py, RKernel.py, 그외 R모듈.py로 이루어져 있습니다.

## 기술 설명
rOS는 각 메이저 버전업마다 신기술을 적용해왔고 업데이트된 내용은 업데이트명 Target.txt 파일로 확인 가능합니다.

rOS EdgeRunner의 DemonSlayer대비 업데이트된 내용은 다음과 같습니다.
> - OpenCV와 TensorFlow의 Thread를 분리하여 성능을 향상시켰습니다.
> 
> - 프로젝트 구조를 변경하여 더욱 효율적인 코드를 작성할 수 있도록 했습니다.
> 
> - 부팅시 심심하지 않도록 새로운 스플래쉬 스크린을 적용했습니다.
> 
> - 초음파센서를 활성화 했습니다.
> 
> - RGPIOD.py를 통하여 자체적인 PWM을 구현했습니다.

rOS는 라이센스비용을 줄이고자 자체개발한 Python IDE인 [SIDE](https://github.com/ellystargram/SIDE)를 이용하여 개발되었습니다.

## 기능
rOS EdgeRunner는 다음과 같은 기능을 제공합니다.
> - **사물 구분**: Tensorflow Lite를 통해 사물을 구분할 수 있습니다.
> 
> - **사물 거리 측정**: 초음파센서와 카메라비전을 이용하여 물체와 떨어진 거리를 측정할 수 있습니다.
> 
> - **간편한 설정 공유**: RKey.RKY 파일을 통해 설정을 공유할 수 있습니다. 이 파일은 누구나 알아보기 쉽도록 제작된 자체개발한 UTF-8 기반의 파일입니다.
> 
> - **RGPIOD**: 자체개발한 RGPIOD를 통해 GPIO를 쉽게 제어할 수 있습니다. PWM도 지원합니다.
> 
> - **TTS**: TTS를 이용해 경고 메시지를 사용자에게 알려줍니다. 저조도주의나 성능저하주의가 대표적인 예입니다.
> 
> - **안드로이드 기기 연결**: 안드로이드 기기와 블루투스로 연결한 다음 [SLD](https://github.com/devMaxTrauma/SLD)를 통해 FindMy 기능이나 색약 색보정이 가능합니다.
> 
> - **Taptic Engine**: Taptic Engine을 통해 사용자에게 진동을 전달할 수 있습니다.
> 
> - **AR**: AR을 통해 사용자에게 보여줍니다. 이를위해 이미지를 양안에 맞게 처리할 수 있는 능력이 있습니다.

## 사용법
ROS.py가 있는 Directory에서 ROS.py를 실행하면 됩니다.

> macOS
>```bash
>~/rOS $ python3 ROS.py
>```
>Linux
>```bash
>~/rOS $ python ROS.py
>```
>Windows
>```cmd
>C:\rOS> python ROS.py
>```

## 사용한 라이브러리
rOS EdgeRunner는 다음과 같은 라이브러리를 사용합니다.
> - **OpenCV**: 그래픽 렌더를 위해 사용합니다.
> - **TensorFlow Lite**: 사물 구분을 위해 사용합니다.
> - **Pygame**: RSound.py를 위해 사용합니다.
> - **threading**: TensorFlow Lite와 OpenCV를 분리하기 위해, 멀티스레딩을 위해 사용합니다.
> - **time**: 초음파센서와 카메라비전을 위해 사용합니다. 또한 자원절약을 위해 사용합니다.
> - **gpiod**: GPIO를 제어하기 위해 RGPIOD에서 사용합니다.
> - **picamera2**: 카메라를 사용하기 위해 사용합니다.
> - **numpy**: TensorFlow Lite에서 사용합니다.
> - **sys**: 시스템을 제어하기 위해 사용합니다.
> - **os**: 시스템을 제어하기 위해 사용합니다.

## 놀라운 사실
rOS EdgeRunner는 다음과 같은 놀라운 사실을 가지고 있습니다.
> - 모든 소스코드줄의 합은 3000줄을 가볍게 넘습니다.
> - rOS EdgeRunner는 github Copilot과 함께 개발되었습니다.
> - 라즈베리파이로 코드를 옮길땐 github repository를 이용하여 코드를 옮겼습니다.

[//]: # (## Introduction)

[//]: # (* rOS is Software for Blind Navigation and Object Detection.)

[//]: # (* rOS is based on python and uses OpenCV and TensorFlow for Object Detection.)

[//]: # (* rOS can calculate distance between user and object.)

[//]: # (* rOS tensorflow and opencv is seperated from main thread to increase performance.)

[//]: # ()
[//]: # (## How to use)

[//]: # (* run ROS.py)