// Test.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include <iostream>
#include "Straight.h"
#include "Vector.h"
#include "Sprial.h"
#include <PQX.h>



int main()
{
    Vector f = Vector(0, 0);
    Angle A = Angle(Degree(0));
        
    //	Straight(double length, Vector& st, Angle& sdir, EITypeID idd = EITypeID::Line, LeftRightEnum lr = LeftRightEnum::NoneLR);

    PQX m1k = PQX("C:/Users/BillHu/source/python/SmartRoadBridgePy/srbpy/test/00-MainLine/M1K-0312/M1K-0312.ICD");
    
    std::cout << std::cout.precision(18) << std::endl;
    std::cout << "输出： " << m1k.get_coordinate(18645.000258927972).Y() << "\n";

}

