#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   kuka_cam_reach_env.py
@Time    :   2021/03/20 14:33:24
@Author  :   Yan Wen
@Version :   1.0
@Contact :   z19040042@s.upc.edu.cn
@License :   (C)Copyright 2021-2022, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

import pybullet as p
import pybullet_data

import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from math import sqrt

import time


import math
import cv2

from colorama import Fore, init, Back

import os

init(autoreset=True)  # this lets colorama takes effect only in current line.


# Otherwise, colorama will let the sentences below 'print(Fore.GREEN+'xx')'
# all become green color.


class KukaCamReachEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50
    }

    def __init__(self, config):

        self.camera_parameters = {
            'width': 960.,
            'height': 720,
            'fov': 60,
            'near': 0.1,
            'far': 100.,
            'eye_position': [0.59, 0, 0.8],
            'target_position': [0.55, 0, 0.05],
            'camera_up_vector':
                [1, 0, 0],  # I really do not know the parameter's effect.
            'light_direction': [
                0.5, 0, 1
            ],  # the direction is from the light source position to the origin of the world frame.
        }

        self.view_matrix = p.computeViewMatrixFromYawPitchRoll(
            cameraTargetPosition=[0.55, 0, 0.05],
            distance=.7,
            yaw=90,
            pitch=-70,
            roll=0,
            upAxisIndex=2)

        self.projection_matrix = p.computeProjectionMatrixFOV(
            fov=self.camera_parameters['fov'],
            aspect=self.camera_parameters['width'] /
                   self.camera_parameters['height'],
            nearVal=self.camera_parameters['near'],
            farVal=self.camera_parameters['far'])

        self.is_render = config["is_render"]
        self.is_good_view = config["is_good_view"]


        if self.is_render:
            p.connect(p.GUI)
        else:
            p.connect(p.DIRECT)

        self.x_low_obs = 0.2
        self.x_high_obs = 0.7
        self.y_low_obs = -0.3
        self.y_high_obs = 0.3
        self.z_low_obs = 0
        self.z_high_obs = 0.55

        self.x_low_action = -0.4
        self.x_high_action = 0.4
        self.y_low_action = -0.4
        self.y_high_action = 0.4
        self.z_low_action = -0.6
        self.z_high_action = 0.3

        p.configureDebugVisualizer(lightPosition=[5, 0, 5])
        p.resetDebugVisualizerCamera(cameraDistance=1.5,
                                     cameraYaw=0,
                                     cameraPitch=-40,
                                     cameraTargetPosition=[0.55, -0.35, 0.2])

        self.action_space = spaces.Box(low=np.array(
            [self.x_low_action, self.y_low_action, self.z_low_action]),
            high=np.array([
                self.x_high_action,
                self.y_high_action,
                self.z_high_action
            ]),
            dtype=np.float32)
        # self.observation_space=spaces.Box(low=np.array([self.x_low_obs,self.y_low_obs,self.z_low_obs]),
        #                              high=np.array([self.x_high_obs,self.y_high_obs,self.z_high_obs]),
        #                              dtype=np.float32)

        self.observation_space = spaces.Box(low=0, high=1., shape=(1, 84, 84))

        self.step_counter = 0

        self.urdf_root_path = pybullet_data.getDataPath()
        # lower limits for null space
        self.lower_limits = [-.967, -2, -2.96, 0.19, -2.96, -2.09, -3.05]
        # upper limits for null space
        self.upper_limits = [.967, 2, 2.96, 2.29, 2.96, 2.09, 3.05]
        # joint ranges for null space
        self.joint_ranges = [5.8, 4, 5.8, 4, 5.8, 4, 6]
        # restposes for null space
        self.rest_poses = [0, 0, 0, 0.5 * math.pi, 0, -math.pi * 0.5 * 0.66, 0]
        # joint damping coefficents
        self.joint_damping = [
            0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001, 0.00001
        ]

        self.init_joint_positions = [
            0.006418, 0.413184, -0.011401, -1.589317, 0.005379, 1.137684,
            -0.006539
        ]

        self.orientation = p.getQuaternionFromEuler(
            [0., -math.pi, math.pi / 2.])

        self.env_name='KukaReachCamEnv-v0'
        self.state_dim=self.observation_space.shape
        self.action_dim=self.action_space.shape[0]
        self.if_discrete=False
        self.target_return=100
        self.max_step = config["max_steps_one_episode"]

        self.seed()
        # self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        # p.connect(p.GUI)
        self.step_counter = 0

        p.resetSimulation()
        # p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 0)
        self.terminated = False
        p.setGravity(0, 0, -10)

        p.addUserDebugLine(
            lineFromXYZ=[self.x_low_obs, self.y_low_obs, 0],
            lineToXYZ=[self.x_low_obs, self.y_low_obs, self.z_high_obs])
        p.addUserDebugLine(
            lineFromXYZ=[self.x_low_obs, self.y_high_obs, 0],
            lineToXYZ=[self.x_low_obs, self.y_high_obs, self.z_high_obs])
        p.addUserDebugLine(
            lineFromXYZ=[self.x_high_obs, self.y_low_obs, 0],
            lineToXYZ=[self.x_high_obs, self.y_low_obs, self.z_high_obs])
        p.addUserDebugLine(
            lineFromXYZ=[self.x_high_obs, self.y_high_obs, 0],
            lineToXYZ=[self.x_high_obs, self.y_high_obs, self.z_high_obs])

        p.addUserDebugLine(
            lineFromXYZ=[self.x_low_obs, self.y_low_obs, self.z_high_obs],
            lineToXYZ=[self.x_high_obs, self.y_low_obs, self.z_high_obs])
        p.addUserDebugLine(
            lineFromXYZ=[self.x_low_obs, self.y_high_obs, self.z_high_obs],
            lineToXYZ=[self.x_high_obs, self.y_high_obs, self.z_high_obs])
        p.addUserDebugLine(
            lineFromXYZ=[self.x_low_obs, self.y_low_obs, self.z_high_obs],
            lineToXYZ=[self.x_low_obs, self.y_high_obs, self.z_high_obs])
        p.addUserDebugLine(
            lineFromXYZ=[self.x_high_obs, self.y_low_obs, self.z_high_obs],
            lineToXYZ=[self.x_high_obs, self.y_high_obs, self.z_high_obs])

        p.loadURDF(os.path.join(self.urdf_root_path, "plane.urdf"),
                   basePosition=[0, 0, -0.65])
        self.kuka_id = p.loadURDF(os.path.join(self.urdf_root_path,
                                               "kuka_iiwa/model.urdf"),
                                  useFixedBase=True)
        table_uid = p.loadURDF(os.path.join(self.urdf_root_path,
                                            "table/table.urdf"),
                               basePosition=[0.5, 0, -0.65])
        p.changeVisualShape(table_uid, -1, rgbaColor=[1, 1, 1, 1])
        # p.loadURDF(os.path.join(self.urdf_root_path, "tray/traybox.urdf"),basePosition=[0.55,0,0])
        # object_id=p.loadURDF(os.path.join(self.urdf_root_path, "random_urdfs/000/000.urdf"), basePosition=[0.53,0,0.02])
        self.object_id = p.loadURDF(os.path.join(self.urdf_root_path,
                                                 "random_urdfs/000/000.urdf"),
                                    basePosition=[
                                        self.np_random.uniform(self.x_low_obs,
                                                               self.x_high_obs),
                                        self.np_random.uniform(self.y_low_obs,
                                                               self.y_high_obs), 0.01
                                    ])

        self.num_joints = p.getNumJoints(self.kuka_id)

        for i in range(self.num_joints):
            p.resetJointState(
                bodyUniqueId=self.kuka_id,
                jointIndex=i,
                targetValue=self.init_joint_positions[i],
            )
        p.stepSimulation()

        return self._process_image()

    def _process_image(self):
        """Convert the RGB pic to gray pic and add a channel 1

        Args:
            image ([type]): [description]
        """

        # ! There will report a error if use pybullet 3.1.7 version (2021-5-16)
        (_, _, px, _, _) = p.getCameraImage(width=960,
                                            height=960,
                                            viewMatrix=self.view_matrix,
                                            projectionMatrix=self.projection_matrix,
                                            renderer=p.ER_BULLET_HARDWARE_OPENGL)

        self.image=px
        #print(self.image.shape)


        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            self.image = cv2.resize(self.image, (84, 84))[None, :, :] / 255.
            return self.image
        else:
            return np.zeros((1, 84, 84))



    def step(self, action):
        # print('action: ',action)
        dv = 0.005
        dx = action[0] * dv
        dy = action[1] * dv
        dz = action[2] * dv

        self.current_pos = p.getLinkState(self.kuka_id, self.num_joints - 1)[4]
        # logging.debug("self.current_pos={}\n".format(self.current_pos))
        self.new_robot_pos = [
            self.current_pos[0] + dx, self.current_pos[1] + dy,
            self.current_pos[2] + dz
        ]
        # logging.debug("self.new_robot_pos={}\n".format(self.new_robot_pos))
        self.robot_joint_positions = p.calculateInverseKinematics(
            bodyUniqueId=self.kuka_id,
            endEffectorLinkIndex=self.num_joints - 1,
            targetPosition=[
                self.new_robot_pos[0], self.new_robot_pos[1],
                self.new_robot_pos[2]
            ],
            targetOrientation=self.orientation,
            jointDamping=self.joint_damping,
        )
        for i in range(self.num_joints):
            p.resetJointState(
                bodyUniqueId=self.kuka_id,
                jointIndex=i,
                targetValue=self.robot_joint_positions[i],
            )
        p.stepSimulation()

        if self.is_good_view:
            time.sleep(0.05)

        self.step_counter += 1
        #  print(Fore.GREEN+'step_counter={}'.format(self.step_counter))

        return self._reward()

    def _reward(self):

        self.robot_state = p.getLinkState(self.kuka_id, self.num_joints - 1)[4]
        # self.object_state=p.getBasePositionAndOrientation(self.object_id)
        # self.object_state=np.array(self.object_state).astype(np.float32)
        #
        self.object_state = np.array(
            p.getBasePositionAndOrientation(self.object_id)[0]).astype(
            np.float32)

        square_dx = (self.robot_state[0] - self.object_state[0]) ** 2
        square_dy = (self.robot_state[1] - self.object_state[1]) ** 2
        square_dz = (self.robot_state[2] - self.object_state[2]) ** 2

        self.distance = sqrt(square_dx + square_dy + square_dz)
        # print(self.distance)

        x = self.robot_state[0]
        y = self.robot_state[1]
        z = self.robot_state[2]

        terminated = bool(x < self.x_low_obs or x > self.x_high_obs
                          or y < self.y_low_obs or y > self.y_high_obs
                          or z < self.z_low_obs or z > self.z_high_obs)

        if terminated:
            reward = -0.1
            self.terminated = True


        elif self.step_counter > self.max_step:
            reward = -0.1
            self.terminated = True

        elif self.distance < 0.1:
            reward = 1
            self.terminated = True
        else:
            reward = 0
            self.terminated = False

        info = {'distance:', self.distance}

        return self._process_image(), reward, self.terminated, {}

    def close(self):
        p.disconnect()



    # def _get_force_sensor_value(self):
    #     force_sensor_value = p.getJointState(bodyUniqueId=self.kuka_id,
    #                                          jointIndex=self.num_joints -
    #                                          1)[2][2]
    #     # the first 2 stands for jointReactionForces, the second 2 stands for Fz,
    #     # the pybullet methods' return is a tuple,so can not
    #     # index it with str like dict. I think it can be improved
    #     # that return value is a dict rather than tuple.
    #     return force_sensor_value


class CustomSkipFrame(gym.Wrapper):
    """ Make a 4 frame skip, so the observation space will change to (4,84,84) from (1,84,84)

    Args:
        gym ([type]): [description]
    """

    def __init__(self, env, skip=4):
        super(CustomSkipFrame, self).__init__(env)
        self.observation_space = spaces.Box(low=0,
                                            high=1.,
                                            shape=(skip, 84, 84))
        self.skip = skip
        self.env_name='KukaReachCamEnv-v0'
        self.state_dim=self.observation_space.shape
        self.action_dim=self.action_space.shape[0]
        self.if_discrete=False
        self.target_return=100

        self.seed()

    def step(self, action):
        total_reward = 0
        states = []
        state, reward, done, info = self.env.step(action)
        for i in range(self.skip):
            if not done:
                state, reward, done, info = self.env.step(action)
                total_reward += reward
                states.append(state)
            else:
                states.append(state)
        states = np.concatenate(states, 0)
        return states.astype(np.float32), reward, done, info

    def reset(self):
        state = self.env.reset()
        states = np.concatenate([state for _ in range(self.skip)], 0)
        # print('states=',states)
        # print('states.shape=',states.shape)
        # states = np.concatenate([state for _ in range(self.skip)],
        #                         0)[:, :, :, None]
        return states.astype(np.float32)


if __name__ == '__main__':
    env_config = {
        "is_render": False,
        "is_good_view": False,
        "max_steps_one_episode": 1000,
    }

    env = KukaCamReachEnv(env_config)
    #env = CustomSkipFrame(env)

    obs = env.reset()
    print(obs)
    print(obs.shape)
    #
    action = env.action_space.sample()
    print('action=', action)
    #
    obs, reward, done, _ = env.step(action)
    print(obs,'\n',obs.shape,'\n',reward,'\n',done)


    # import matplotlib.pyplot as plt
    # import numpy as np
    #
    # img = np.moveaxis(obs,0,-1)
    # print(img.shape)
    #
    # plt.imshow(img[:,:,:3])
    # plt.show()

    # all the below are some debug codes, if you have interests, look through.

    # b=a[:,:,:3]
    # c=b.transpose((2,0,1))
    # #c=b
    # d=np.ascontiguousarray(c,dtype=np.float32)/255
    # e=torch.from_numpy(d)
    # resize=T.Compose([T.ToPILImage(),
    #                   T.Resize(40,interpolation=Image.CUBIC),
    #                     T.ToTensor()])

    # f=resize(e).unsqueeze(0)
    # #print(f)
    # # g=f.unsqueeze(0)
    # # print(g)
    # #f.transpose((2,0,1))

    # plt.imshow(f.cpu().squeeze(0).permute(1, 2, 0).numpy(),
    #        interpolation='none')

    # #plt.imshow(f)
    # plt.show()

    # resize = T.Compose([T.ToPILImage(),
    #                 T.Resize(40, interpolation=Image.CUBIC),
    #                 T.ToTensor()])

# print(env)
# print(env.observation_space.shape)
# print(env.observation_space.sample())

# for i in range(10):
#     a=env.reset()
#     b=a[:,:,:3]
#     """
#     matplotlib.pyplot.imshow(X, cmap=None, norm=None, aspect=None, interpolation=None,
#     alpha=None, vmin=None, vmax=None, origin=None, extent=None, *, filternorm=True,
#     filterrad=4.0, resample=None, url=None, data=None, **kwargs)

#     Xarray-like or PIL image
#     The image data. Supported array shapes are:

#     (M, N): an image with scalar data. The values are mapped to colors using normalization and a colormap. See parameters norm, cmap, vmin, vmax.
#     (M, N, 3): an image with RGB values (0-1 float or 0-255 int).
#     (M, N, 4): an image with RGBA values (0-1 float or 0-255 int), i.e. including transparency.
#     The first two dimensions (M, N) define the rows and columns of the image.
#     Out-of-range RGB(A) values are clipped.
#     """
#     plt.imshow(b)
#     plt.show()
#     time.sleep(1)

# for i in range(720):
#     for j in range(720):
#         for k in range(3):
#             if not a[i][j][k]==b[i][j][k]:
#                 print(Fore.RED+'there is unequal')
#                 raise ValueError('there is unequal.')
# print('check complete')

# print(a)
# force_sensor=env.run_for_debug([0.6,0.0,0.03])
# print(Fore.RED+'after force sensor={}'.format(force_sensor))
# print(env.action_space.sample())

# sum_reward=0
# for i in range(10):
#     env.reset()
#     for i in range(2000):
#         action=env.action_space.sample()
#         #action=np.array([0,0,0.47-i/1000])
#         obs,reward,done,info=env.step(action)
#       #  print("i={},\naction={},\nobs={},\ndone={},\n".format(i,action,obs,done,))
#         print(colored("reward={},info={}".format(reward,info),"cyan"))
#        # print(colored("info={}".format(info),"cyan"))
#         sum_reward+=reward
#         if done:
#             break
#        # time.sleep(0.1)
# print()
# print(sum_reward)
