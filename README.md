# **rOS EdgeRunner**

## 오픈 소스 소개

rOS는 모든 하위 버전을 포함하여 오픈소스 프로젝트입니다. 누구나 코드를 참고하거나 수정할 수 있습니다.

rOS를 어떤 방식으로든 사용할 경우, 다음 조건을 준수해야 합니다:

> ### A. 출처 표기
> rOS 코드를 사용하는 모든 프로젝트와 발표에서는 **반드시 출처를 명시**해야 합니다. 출처를 명시하지 않을 경우, 코드에 대한 사용 권한을 상실하게 되며, 이를 기반으로 한 **소유권을 주장할 수 없습니다**.
> 출처 표시는 다음 위치에 포함되어야 합니다:
> - 코드 파일 주석
> - README 파일
> - 프로젝트의 사용자 인터페이스(해당하는 경우)
> - 학교 또는 학술 발표 자료
>
> ---
> 
> ### B. 비상업적 및 윤리적 사용
> rOS는 기본적으로 모두에게 오픈소스 프로젝트로 제공됩니다. 그러나 **상업적 목적**이나 **비윤리적인 목적**으로 사용되는 것을 금지합니다. 상업적 사용을 원할 경우, devMaxTrauma Inc.와 개발자의 사전 서면 동의가 필요합니다.
> 
> ---
> 
> ### C. 수정 코드에 대한 소유권
> rOS 코드를 참고하거나 기반으로 수정한 코드를 개발한 모든 개인 또는 단체는 해당 코드에 대해 **devMaxTrauma. Inc.** 와 개발자가 소유권을 행사할 수 있습니다. 수정된 코드는 동일한 라이선스 조건을 따라야 하며, **클로즈드소스**로 전환할 수 없습니다.
> 
> ---
> 
> ### D. 책임 면책
> 이 프로젝트의 코드는 **있는 그대로 제공**되며, 사용 중 발생할 수 있는 문제에 대해 어떠한 책임도 지지 않습니다. 코드 사용으로 인해 발생하는 법적 문제, 손해, 또는 기타 불이익에 대해 **개발자는 책임을 지지 않으며**, 모든 책임은 사용자에게 있습니다.
> 
> ---
> 
> ### E. 보증 없음
> rOS 코드는 **어떠한 보증도 제공하지 않습니다**. 이 코드는 명시적이든 묵시적이든 특정 목적에 대한 보증 없이 제공됩니다. 코드가 기대한 대로 동작하지 않거나, 문제가 발생해도 개발자는 이에 대한 책임이 없습니다.
> 
> ---
> 
> ### F. 배포 조건
> rOS 코드를 수정하거나 배포할 경우, 이 라이선스 조건을 **동일하게 유지**해야 합니다. 이 프로젝트에 기여하는 모든 코드 역시 동일한 조건에 따라 배포되어야 합니다.
> 
> ---
> 
> ### G. 동의
> rOS를 사용하는 경우, 위의 모든 조건에 동의하는 것으로 간주합니다. 출처를 명시하지 않은 경우, 사용자는 해당 코드의 권리 및 소유권을 주장할 수 없으며, 법적 제재의 대상이 될 수 있습니다.


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
---
>Linux
>```bash
>~/rOS $ python ROS.py
>```
---
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
