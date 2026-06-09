//
// Created by BillHu on 2020/11/12.
//
#include <iostream>
#include <vector>
// #include "gfunc.h"
#include "PQX.h"
#include <iomanip>

int main(int argc, char *argv[]) {
    PQX fu = PQX(L"C:\\Users\\bill\\source\\repos\\SmartRoadBridgePy\\docs\\test_data\\M.ICD");

    double pks[] = {2057.474, 2102.474};
    for (double pk : pks) {
        Vector c = fu.get_coordinate(pk);
        std::cout << std::fixed << std::setprecision(6)
                  << "pk=" << pk << " -> X=" << c.X() << ", Y=" << c.Y() << std::endl;
    }
    return 0;
}
