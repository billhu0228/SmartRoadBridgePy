//
// Created by BillHu on 2020/11/12.
//
#include <iostream>
#include <vector>
// #include "gfunc.h"
#include "PQX.h"

int main(int argc, char *argv[]) {
    PQX fu = PQX(L"G:\\20191213-�����Ǹ߼���ʩ��ͼ���(19406)\\01 ǰ������\\EI Data\\00-MainLine\\L1K-0926\\L1K-0926.ICD");

    std::wcout << fu.ICDText[3] << std::endl;
}