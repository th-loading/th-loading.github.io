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

// cwise 
v = v.cwiseProduct(w);
// dot product
a.dot(b)

// -0.707107 2.12132 0
```

## Assignment 1

正交投影只需要将长方体内的所有点都伸缩到标准立方体上，不需要处理成二维点。

? z轴正交投影伸缩的比例并不影响成像，也不需要对z轴做平移 

实际处理时直接舍弃了z轴，点z值的正负大小不影响成像

```c++
// void rst::rasterizer::draw_line(Eigen::Vector3f begin, Eigen::Vector3f end)
// draw_line 只考虑x和y
```

？生成的坐标不在立方体内也能成像，(3.58518, 0, x,  -2) 

没有考虑MVP变换的View（只改变了z轴），直接在projection上debug。

点向后平移后，映射在[-n, -f] 之间的位置出现了变化

```c++
// void rst::rasterizer::draw(rst::pos_buf_id pos_buffer, rst::ind_buf_id ind_buffer, rst::Primitive type)

// width 700 
// rst::rasterizer r(700, 700);

// 角度变换矩阵
void rst::rasterizer::set_model(const Eigen::Matrix4f& m)
{
    model = m;
}

Eigen::Matrix4f mvp = projection * view * model;
Eigen::Vector4f v[] = {
        mvp * to_vec4(buf[i[0]], 1.0f),
        mvp * to_vec4(buf[i[1]], 1.0f),
        mvp * to_vec4(buf[i[2]], 1.0f)
};

for (auto& vec : v) {
    // 齐次坐标标准化
    vec /= vec.w();
}

for (auto & vert : v)
{
    // 具体的作图大于0 [0 - width] vert.x() 需要在[-1, 1]
    vert.x() = 0.5*width*(vert.x()+1.0);
    vert.y() = 0.5*height*(vert.y()+1.0);
    vert.z() = vert.z() * f1 + f2;
}

```

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

## Assignment 2

bounding box, 不用考虑坐标是否符合边界

```c++
void rst::rasterizer::rasterize_triangle(const Triangle& t) {
    auto v = t.toVector4();
    
    // TODO : Find out the bounding box of current triangle.
    // iterate through the pixel and find if the current pixel is inside the triangle
    
    // bounding box 不用考虑坐标是否符合边界
    int min_x = std::min(v[0].x(), std::min(v[1].x(), v[2].x()));
    int max_x = std::max(v[0].x(), std::max(v[1].x(), v[2].x()));
    int min_y = std::min(v[0].y(), std::min(v[1].y(), v[2].y()));
    int max_y = std::max(v[0].y(), std::max(v[1].y(), v[2].y()));
    for (int x = min_x; x <= max_x; ++x) {
        for (int y = min_y; y <= max_y; ++y) {
            if (insideTriangle(x, y, t.v)) {
                // 借助重心坐标, 只看x, y 
                auto [alpha, beta, gamma] = computeBarycentric2D(x, y, t.v);
                float w_reciprocal = 1.0/(alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
                float z_interpolated = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
                z_interpolated *= w_reciprocal;
                // 深度初始化为无穷大 
                // ... 还是负数 ...
                // std::cout << z_interpolated << "\n";
                if (-z_interpolated < depth_buf[get_index(x, y)]) {
                    depth_buf[get_index(x, y)] = -z_interpolated;
                    set_pixel(Eigen::Vector3f(x, y, -z_interpolated), t.getColor());
                }
            }
        }
    }
}

static bool cross_product(int x, int y, int x1, int y1, int x2, int y2) {
    // (x - x1, y - y1) (x1 - x2, y1 - y2)
    return (x - x1) * (y1 - y2) - (x1 - x2) * (y - y1) > 0;
}

static bool insideTriangle(int x, int y, const Vector3f* _v)
{   
    // TODO : Implement this function to check if the point (x, y) is inside the triangle represented by _v[0], _v[1], _v[2]
    bool s1 = cross_product(x, y, _v[0].x(), _v[0].y(), _v[1].x(), _v[1].y());
    bool s2 = cross_product(x, y, _v[1].x(), _v[1].y(), _v[2].x(), _v[2].y());
    bool s3 = cross_product(x, y, _v[2].x(), _v[2].y(), _v[0].x(), _v[0].y());
    return s1 == s2 && s2 == s3;
}
```

## Assignment 3

```c++
// 基本的设置 rasterizer.cpp
for (int x = min_x; x <= max_x; ++x) {
    for (int y = min_y; y <= max_y; ++y) {
        if (insideTriangle(x, y, t.v)) {
            // 借助重心坐标, 只看x, y 
            auto [alpha, beta, gamma] = computeBarycentric2D(x, y, t.v);
            float w_reciprocal = 1.0/(alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
            float z_interpolated = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
            z_interpolated *= w_reciprocal;
            auto interpolated_color = alpha * t.color[0] + beta * t.color[1] + gamma * t.color[2];
            
            // 注意向量处理
            auto interpolated_normal = (alpha * t.normal[0] + beta * t.normal[1] + gamma * t.normal[2]).normalized();
            
            auto interpolated_texcoords = alpha * t.tex_coords[0] + beta * t.tex_coords[1] + gamma * t.tex_coords[2];
            auto interpolated_shadingcoords = alpha * view_pos[0] + beta * view_pos[1] + gamma * view_pos[2];

            // 深度初始化为无穷大
            // std::cout << z_interpolated << "\n";
            if (-z_interpolated < depth_buf[get_index(x, y)]) {
                fragment_shader_payload payload( interpolated_color, interpolated_normal.normalized(), interpolated_texcoords, texture ? &*texture : nullptr);
                depth_buf[get_index(x, y)] = -z_interpolated;
                
                
                // 漏了一行。。。
                // 效果差不多。。。
                // 很难DEBUG。。。
				payload.view_pos = interpolated_shadingcoords;
				// 以为问题在main函数中的插值实现。。。
                
                // payload存储必要的插值信息（第一步插值），根据shader生成颜色
                // shader还能进行texture坐标下的插值（第二次插值）
                auto pixel_color = fragment_shader(payload);
                // std::cout << pixel_color << "\n";
                set_pixel(Eigen::Vector2i(x, y), pixel_color);
            }
        }
    }
}

```

```c++
Eigen::Vector3f phong_fragment_shader(const fragment_shader_payload& payload)
{
    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = payload.color;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{{20, 20, 20}, {500, 500, 500}};
    auto l2 = light{{-20, 20, 0}, {500, 500, 500}};

    std::vector<light> lights = {l1, l2};
    Eigen::Vector3f amb_light_intensity{10, 10, 10};
    Eigen::Vector3f eye_pos{0, 0, 10};

    float p = 150;

    Eigen::Vector3f color = payload.color;
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;
    // normal = -normal;

    Eigen::Vector3f result_color = {0, 0, 0};
    for (auto& light : lights)
    {
        // TODO: For each light source in the code, calculate what the *ambient*, *diffuse*, and *specular* 
        // components are. Then, accumulate that result on the *result_color* object.
        Eigen::Vector3f ambient, diffuse, specular, light_vec, view_vec;
        
        // 注意normalized()
        light_vec = (light.position - point).normalized();
        view_vec = (eye_pos - point).normalized();
        float ecos1 = std::max(0.0f, normal.dot(light_vec));
        
        float ecos2 = std::pow(std::max(0.0f, normal.dot((light_vec + view_vec).normalized())), p);
        
        // 可以自乘dot实现
        float rsquare = (light.position - point).squaredNorm();
        
        ambient = ka.cwiseProduct(amb_light_intensity);
        diffuse = ecos1 * kd.cwiseProduct((light.intensity/rsquare));
        specular = ecos2 * ks.cwiseProduct((light.intensity/rsquare));
        result_color += diffuse + specular + ambient;
    }

    return result_color * 255.f;
}

```

```c++
// ./Rasterizer output.png texture
if (payload.texture)
{
    // TODO: Get the texture value at the texture coordinates of the current fragment
    texture_color = payload.texture->getColor(payload.tex_coords.x(), payload.tex_coords.y());
}
```

```c++
Eigen::Vector3f bump_fragment_shader(const fragment_shader_payload& payload)
{
    
    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = payload.color;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{{20, 20, 20}, {500, 500, 500}};
    auto l2 = light{{-20, 20, 0}, {500, 500, 500}};

    std::vector<light> lights = {l1, l2};
    Eigen::Vector3f amb_light_intensity{10, 10, 10};
    Eigen::Vector3f eye_pos{0, 0, 10};

    float p = 150;

    Eigen::Vector3f color = payload.color; 
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;


    float kh = 0.2, kn = 0.1;

    // TODO: Implement bump mapping here
    // Let n = normal = (x, y, z)
    // Vector t = (x*y/sqrt(x*x+z*z),sqrt(x*x+z*z),z*y/sqrt(x*x+z*z))
    // Vector b = n cross product t
    // Matrix TBN = [t b n]
    // dU = kh * kn * (h(u+1/w,v)-h(u,v))
    // dV = kh * kn * (h(u,v+1/h)-h(u,v))
    // Vector ln = (-dU, -dV, 1)
    // Normal n = normalize(TBN * ln)
    float x = normal[0], y = normal[1], z = normal[2];
    Eigen::Vector3f t = {x*y/sqrt(x*x+z*z), sqrt(x*x+z*z), z*y/sqrt(x*x+z*z)};
    Eigen::Vector3f b = normal.cross(t);
    Matrix3f TBN;
    TBN.col(0) = t;
    TBN.col(1) = b;
    TBN.col(2) = normal;
    // dU = kh * kn * (h(u+1/w, v)- h(u,v));
    float dU = kh * kn * (payload.texture->getColor(payload.tex_coords.x() + 1.0f/payload.texture->width, payload.tex_coords.y()).norm() - payload.texture->getColor(payload.tex_coords.x(), payload.tex_coords.y()).norm());
    float dV = kh * kn * (payload.texture->getColor(payload.tex_coords.x(), payload.tex_coords.y() + 1.0f/payload.texture->height).norm() - payload.texture->getColor(payload.tex_coords.x(), payload.tex_coords.y()).norm());
    Vector3f ln = {-dU, -dV, 1};
    normal = (TBN * ln).normalized();
    Eigen::Vector3f result_color = {0, 0, 0};
    result_color = normal;

    return result_color * 255.f;
}
```

```c++
Eigen::Vector3f displacement_fragment_shader(const fragment_shader_payload& payload)
{
    
    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = payload.color;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{{20, 20, 20}, {500, 500, 500}};
    auto l2 = light{{-20, 20, 0}, {500, 500, 500}};

    std::vector<light> lights = {l1, l2};
    Eigen::Vector3f amb_light_intensity{10, 10, 10};
    Eigen::Vector3f eye_pos{0, 0, 10};

    float p = 150;

    Eigen::Vector3f color = payload.color; 
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;

    float kh = 0.2, kn = 0.1;
    Eigen::Vector3f result_color = {0, 0, 0};

    // TODO: Implement displacement mapping here
    // Let n = normal = (x, y, z)
    // Vector t = (x*y/sqrt(x*x+z*z),sqrt(x*x+z*z),z*y/sqrt(x*x+z*z))
    // Vector b = n cross product t
    // Matrix TBN = [t b n]
    // dU = kh * kn * (h(u+1/w,v)-h(u,v))
    // dV = kh * kn * (h(u,v+1/h)-h(u,v))
    // Vector ln = (-dU, -dV, 1)
    // Position p = p + kn * n * h(u,v)
    // Normal n = normalize(TBN * ln)
    float x = normal[0], y = normal[1], z = normal[2];
    Eigen::Vector3f t = {x*y/sqrt(x*x+z*z), sqrt(x*x+z*z), z*y/sqrt(x*x+z*z)};
    Eigen::Vector3f b = normal.cross(t);
    Matrix3f TBN;
    TBN.col(0) = t;
    TBN.col(1) = b;
    TBN.col(2) = normal;
    // dU = kh * kn * (h(u+1/w, v)- h(u,v));
    float dU = kh * kn * (payload.texture->getColor(payload.tex_coords.x() + 1.0f/payload.texture->width, payload.tex_coords.y()).norm() - payload.texture->getColor(payload.tex_coords.x(), payload.tex_coords.y()).norm());
    float dV = kh * kn * (payload.texture->getColor(payload.tex_coords.x(), payload.tex_coords.y() + 1.0f/payload.texture->height).norm() - payload.texture->getColor(payload.tex_coords.x(), payload.tex_coords.y()).norm());
    Vector3f ln = {-dU, -dV, 1};
    point = point + kn * normal * payload.texture->getColor(payload.tex_coords.x(), payload.tex_coords.y()).norm();
    normal = (TBN * ln).normalized();

    for (auto& light : lights)
    {
        // TODO: For each light source in the code, calculate what the *ambient*, *diffuse*, and *specular* 
        // components are. Then, accumulate that result on the *result_color* object.

        Eigen::Vector3f ambient, diffuse, specular, light_vec, view_vec;
        light_vec = (light.position - point).normalized();
        view_vec = (eye_pos - point).normalized();
        float ecos1 = std::max(0.0f, normal.dot(light_vec));
        float ecos2 = std::pow(std::max(0.0f, normal.dot((light_vec + view_vec).normalized())), p);
        float rsquare = (light.position - point).squaredNorm();
        ambient = ka.cwiseProduct(amb_light_intensity);
        diffuse = ecos1 * kd.cwiseProduct((light.intensity/rsquare));
        specular = ecos2 * ks.cwiseProduct((light.intensity/rsquare));
        result_color += diffuse + specular + ambient;        
    }

    return result_color * 255.f;
}
```

