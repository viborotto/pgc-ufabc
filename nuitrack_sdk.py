from PyNuitrack import py_nuitrack
import cv2
from itertools import cycle
import numpy as np
import time

def update_global_timestamp(start_time):
    global global_timestamp
    # Atualiza o global_timestamp com o tempo decorrido em microssegundos
    global_timestamp = int((time.time() - start_time) * 1e6)

def draw_face(image):
	if not data_instance:
		return
	for instance in data_instance["Instances"]:
		line_color = (59, 164, 225)
		text_color = (59, 255, 255)
		if 'face' in instance.keys():
			bbox = instance["face"]["rectangle"]
		else:
			return
		x1 = (round(bbox["left"]), round(bbox["top"]))
		x2 = (round(bbox["left"]) + round(bbox["width"]), round(bbox["top"]))
		x3 = (round(bbox["left"]), round(bbox["top"]) + round(bbox["height"]))
		x4 = (round(bbox["left"]) + round(bbox["width"]), round(bbox["top"]) + round(bbox["height"]))
		cv2.line(image, x1, x2, line_color, 3)
		cv2.line(image, x1, x3, line_color, 3)
		cv2.line(image, x2, x4, line_color, 3)
		cv2.line(image, x3, x4, line_color, 3)
		cv2.putText(image, "User {}".format(instance["id"]), 
		x1, cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
		cv2.putText(image, "{} {}".format(instance["face"]["gender"],int(instance["face"]["age"]["years"])), 
		x3, cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)

def draw_skeleton(image):
	point_color = (59, 164, 0)
	for skel in data.skeletons:
		for el in skel[1:]:
			x = (round(el.projection[0]), round(el.projection[1]))
			cv2.circle(image, x, 8, point_color, -1)

# Adiciona a variável global para o timestamp
global_timestamp = 0
nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()

# Captura o timestamp de início para calcular o tempo decorrido
start_time = time.time()

devices = nuitrack.get_device_list()
for i, dev in enumerate(devices):
	print(dev.get_name(), dev.get_serial_number())
	if i == 0:
		dev.activate("license:55157:XuPgpkguyKV9oPG6") #you can activate device using python api
		print(dev.get_activation())
		nuitrack.set_device(dev)


print(nuitrack.get_version())
print(nuitrack.get_license())

nuitrack.create_modules()
nuitrack.run()

modes = cycle(["depth", "color"])
mode = next(modes)
print("Timestamp,"
      "Cabeça X,Cabeça Y,Cabeça Z,"
      "Pescoço X,Pescoço Y,Pescoço Z,"
      "Tronco X,Tronco Y,Tronco Z,"
      "Cintura X,Cintura Y,Cintura Z,"
      "Ombro Esquerdo X,Ombro Esquerdo Y,Ombro Esquerdo Z,"
      "Ombro Direito X,Ombro Direito Y,Ombro Direito Z,"
      "Cotovelo Esquerdo X,Cotovelo Esquerdo Y,Cotovelo Esquerdo Z,"
      "Cotovelo Direito X,Cotovelo Direito Y,Cotovelo Direito Z,"
      "Pulso Esquerdo X,Pulso Esquerdo Y,Pulso Esquerdo Z,"
      "Pulso Direito X,Pulso Direito Y,Pulso Direito Z,"
      "Quadril Esquerdo X,Quadril Esquerdo Y,Quadril Esquerdo Z,"
      "Quadril Direito X,Quadril Direito Y,Quadril Direito Z,"
      "Joelho Esquerdo X,Joelho Esquerdo Y,Joelho Esquerdo Z,"
      "Joelho Direito X,Joelho Direito Y,Joelho Direito Z,"
      "Tornozelo Esquerdo X,Tornozelo Esquerdo Y,Tornozelo Esquerdo Z,"
      "Tornozelo Direito X,Tornozelo Direito Y,Tornozelo Direito Z,"
      "Mao Esquerda X,Mao Esquerda Y,Mao Esquerda Z,"
      "Mao Direita X,Mao Direita Y,Mao Direita Z,"
      "Colarinho Esquerdo X,Colarinho Esquerdo Y,Colarinho Esquerdo Z,"
      "Colarinho Direito X,Colarinho Direito Y,Colarinho Direito Z,"
      )
while 1:
    key = cv2.waitKey(1)
    nuitrack.update()
    data = nuitrack.get_skeleton()
    # print(f"TImestamp FORA: {global_timestamp}")
    data_instance = nuitrack.get_instance()

    if data is not None and hasattr(data, 'skeletons'):
        # Atualiza o timestamp global com o tempo decorrido
        update_global_timestamp(start_time)
        for skeleton in data.skeletons:
            try:

                joint_types = [
                    "head",
                    "neck",
                    "torso",
                    "waist",
                    "left_collar",
                    "left_shoulder",
                    "left_elbow",
                    "left_wrist",
                    "left_hand",
                    "right_collar",
                    "right_shoulder",
                    "right_elbow",
                    "right_wrist",
                    "right_hand",
                    "left_hip",
                    "left_knee",
                    "left_ankle",
                    "right_hip",
                    "right_knee",
                    "right_ankle"
                ]


                # Substitua os prints dentro do try block pelo seguinte:
                head_x, head_y, head_z = skeleton.head.real
                neck_x, neck_y, neck_z = skeleton.neck.real
                torso_x, torso_y, torso_z = skeleton.torso.real
                waist_x, waist_y, waist_z = skeleton.waist.real
                left_shoulder_x, left_shoulder_y, left_shoulder_z = skeleton.left_shoulder.real
                right_shoulder_x, right_shoulder_y, right_shoulder_z = skeleton.right_shoulder.real
                left_elbow_x, left_elbow_y, left_elbow_z = skeleton.left_elbow.real
                right_elbow_x, right_elbow_y, right_elbow_z = skeleton.right_elbow.real
                left_wrist_x, left_wrist_y, left_wrist_z = skeleton.left_wrist.real
                right_wrist_x, right_wrist_y, right_wrist_z = skeleton.right_wrist.real
                left_hip_x, left_hip_y, left_hip_z = skeleton.left_hip.real
                right_hip_x, right_hip_y, right_hip_z = skeleton.right_hip.real

                left_knee_x, left_knee_y, left_knee_z = skeleton.left_knee.real
                right_knee_x, right_knee_y, right_knee_z = skeleton.right_knee.real
                left_ankle_x, left_ankle_y, left_ankle_z = skeleton.left_ankle.real
                right_ankle_x, right_ankle_y, right_ankle_z = skeleton.right_ankle.real
                left_hand_x, left_hand_y, left_hand_z = skeleton.left_hand.real
                right_hand_x, right_hand_y, right_hand_z = skeleton.right_hand.real
                left_collar_x, left_collar_y, left_collar_z = skeleton.left_collar.real
                right_collar_x, right_collar_y, right_collar_z = skeleton.right_collar.real
                print(f"{global_timestamp},"
                    f"{head_x},{head_y},{head_z},"
                    f"{neck_x},{neck_y},{neck_z},"
                    f"{torso_x},{torso_y},{torso_z},"
                    f"{waist_x},{waist_y},{waist_z},"
                    f"{left_shoulder_x},{left_shoulder_y},{left_shoulder_z},"
                    f"{right_shoulder_x},{right_shoulder_y},{right_shoulder_z},"
                    f"{left_elbow_x},{left_elbow_y},{left_elbow_z},"
                    f"{right_elbow_x},{right_elbow_y},{right_elbow_z},"
                    f"{left_wrist_x},{left_wrist_y},{left_wrist_z},"
                    f"{right_wrist_x},{right_wrist_y},{right_wrist_z},"
                    f"{left_hip_x},{left_hip_y},{left_hip_z},"
                    f"{right_hip_x},{right_hip_y},{right_hip_z},"

                    f"{left_knee_x},{left_knee_y},{left_knee_z},"
                    f"{right_knee_x},{right_knee_y},{right_knee_z},"
                    f"{left_ankle_x},{left_ankle_y},{left_ankle_z},"
                    f"{right_ankle_x},{right_ankle_y},{right_ankle_z},"
                    f"{left_hand_x},{left_hand_y},{left_hand_z},"
                    f"{right_hand_x},{right_hand_y},{right_hand_z},"
                    f"{left_collar_x},{left_collar_y},{left_collar_z},"
                    f"{right_collar_x},{right_collar_y},{right_collar_z}"
                    )

            except AttributeError as e:
                print(f"Erro ao acessar dados do esqueleto: {e}")

    img_depth = nuitrack.get_depth_data()
    if img_depth.size:
        cv2.normalize(img_depth, img_depth, 0, 255, cv2.NORM_MINMAX)
        img_depth = np.array(cv2.cvtColor(img_depth, cv2.COLOR_GRAY2RGB), dtype=np.uint8)
        img_color = nuitrack.get_color_data()
        draw_skeleton(img_depth)
        draw_skeleton(img_color)
        draw_face(img_depth)
        draw_face(img_color)
        if key == 32:
            mode = next(modes)
        if mode == "depth":
            cv2.imshow('Image', img_depth)
        if mode == "color":
            if img_color.size:
                cv2.imshow('Image', img_color)

    if key == 27:  # Esc key to stop
        break

nuitrack.release()
