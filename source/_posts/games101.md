---
title: Games101 
date: 2023-09-25 19:59:01 
tags: Game
---

## Assignment 0

给定一个点 P = (2，1)，将该点绕原点先逆时针旋转 45◦ ，再平移 (1，2)，计算出变换后点的坐标（要求用齐次坐标进行计算）。

仿射变换 - 三维点 (2, 1, 0)  

```c++
// Eigen库的api
// 确定矩阵的维度即可读入matrix
Eigen :: Matrix3f i,j;
i << 1.0 , 2.0 , 3.0, 
     4.0, 5.0, 6.0;

// 运算 运算符重载代表直接的运算。

#include<cmath>
#include<eigen3/Eigen/Core>
#include<eigen3/Eigen/Dense>
#include<iostream>
 
Eigen::Matrix3f Rotate_matrix(const float degree) {
    Eigen::Matrix3f v;
    float radian = degree * (float)M_PI / 180.0f;
    v << std::cos(radian), -std::sin(radian), 0,
        std::sin(radian), std::cos(radian), 0,
        0, 0, 1;
    return v; 
}

Eigen::Matrix3f shift_matrix(const float x, const float y) {
    Eigen::Matrix3f v;
    v << 1, 0, x,
        0, 1, y,
        0, 0, 1;
    return v; 
}

Eigen::Vector3f x(a, b, 0), y;
Eigen::Matrix3f v0 = Rotate_matrix(45);
Eigen::Matrix3f v1 = shift_matrix(1, 2);
// 矩阵乘法
y = v1 * v0 * x;
std::cout << y << std::endl;

// -0.707107 2.12132 0
```

## Assignment 1

假定了在z轴向内看，不需要额外调整视角，只需要调整观测的位置，默认的正交变换的长方体的中心已经位于原点上。

正交变换只需要将长方体内的所有点都伸缩到标准立方体上，剩余的像素点选择使用Z-buffer，不需要处理。

```c++
#include "Triangle.hpp"
#include "rasterizer.hpp"
#include <eigen3/Eigen/Eigen>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <cmath>

constexpr double MY_PI = 3.1415926;


Eigen::Matrix4f get_view_matrix(Eigen::Vector3f eye_pos)
{
    Eigen::Matrix4f view = Eigen::Matrix4f::Identity();

    Eigen::Matrix4f translate;
    // 视角平移到原点
    translate << 1, 0, 0, -eye_pos[0],
                 0, 1, 0, -eye_pos[1], 
                 0, 0, 1, -eye_pos[2], 
                 0, 0, 0, 1;

    view = translate * view;

    return view;
}

Eigen::Matrix4f get_model_matrix(float rotation_angle)
{
    // 只考虑使得物体沿z轴旋转的视角变换
    Eigen::Matrix4f model = Eigen::Matrix4f::Identity();

    // TODO: Implement this function
    // Create the model matrix for rotating the triangle around the Z axis.
    // Then return it.

    // 绕z轴 z不变 （x, y, z, 1)
    Eigen::Matrix4f rotate;
    // 注意 angle -> radian
    float rotation_radian = rotation_angle * MY_PI / 180.0f;
    rotate << std::cos(rotation_radian), -std::sin(rotation_radian), 0, 0,
                              std::sin(rotation_radian), std::cos(rotation_radian), 0, 0,
                              0, 0, 1, 0,
                              0, 0, 0, 1;

    model = rotate * model;

    return model;
}

Eigen::Matrix4f get_projection_matrix(float eye_fov, float aspect_ratio,
                                      float zNear, float zFar)
{
    // Students will implement this function

    Eigen::Matrix4f projection = Eigen::Matrix4f::Identity();

    // TODO: Implement this function
    // Create the projection matrix for the given parameters.
    // Then return it.

    // M_正交 * M_project

    Eigen::Matrix4f projToOrth, orth;
    projToOrth << -zNear, 0, 0, 0,
                  0, -zNear, 0, 0,
                  0, 0, -zNear - zFar, -zNear * zFar, 
                  0, 0, 1, 0;
    
    float t = std::tan(eye_fov/2) * std::abs(zNear);
    float r = aspect_ratio * t;
    orth << 1 / r, 0, 0, 0, 
            0, 1 / t, 0, 0,
            0, 0, 2 / (zFar - zNear), 0,
            0, 0, 0, 1;

    projection =  projection * orth * projToOrth;

    return projection;
}

int main(int argc, const char** argv)
{
    float angle = 0;
    bool command_line = false;
    std::string filename = "output.png";

    if (argc >= 3) {
        command_line = true;
        angle = std::stof(argv[2]); // -r by default
        if (argc == 4) {
            filename = std::string(argv[3]);
        }
    }

    rst::rasterizer r(700, 700);

    Eigen::Vector3f eye_pos = {0, 0, 5};

    std::vector<Eigen::Vector3f> pos{{2, 0, -2}, {0, 2, -2}, {-2, 0, -2}};

    std::vector<Eigen::Vector3i> ind{{0, 1, 2}};

    auto pos_id = r.load_positions(pos);
    auto ind_id = r.load_indices(ind);

    int key = 0;
    int frame_count = 0;

    if (command_line) {
        r.clear(rst::Buffers::Color | rst::Buffers::Depth);
		// pipeline 
        r.set_model(get_model_matrix(angle));
        r.set_view(get_view_matrix(eye_pos));
        r.set_projection(get_projection_matrix(45, 1, 0.1, 50));

        r.draw(pos_id, ind_id, rst::Primitive::Triangle);
        cv::Mat image(700, 700, CV_32FC3, r.frame_buffer().data());
        image.convertTo(image, CV_8UC3, 1.0f);

        cv::imwrite(filename, image);

        return 0;
    }

    while (key != 27) {
        r.clear(rst::Buffers::Color | rst::Buffers::Depth);

        r.set_model(get_model_matrix(angle));
        r.set_view(get_view_matrix(eye_pos));
        r.set_projection(get_projection_matrix(45, 1, 0.1, 50));

        r.draw(pos_id, ind_id, rst::Primitive::Triangle);

        cv::Mat image(700, 700, CV_32FC3, r.frame_buffer().data());
        image.convertTo(image, CV_8UC3, 1.0f);
        cv::imshow("image", image);
        key = cv::waitKey(10);

        std::cout << "frame count: " << frame_count++ << '\n';

        if (key == 'a') {
            angle += 10;
        }
        else if (key == 'd') {
            angle -= 10;
        }
    }

    return 0;
}

```

### Assignment 2
