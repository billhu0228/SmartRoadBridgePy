//
// Verify analytic get_dir on M.ICD
//
#include <iostream>
#include <vector>
#include <cmath>
#include "PQX.h"
#include <iomanip>

int main(int argc, char *argv[]) {
    PQX fu = PQX(L"C:\\Users\\bill\\source\\repos\\SmartRoadBridgePy\\docs\\test_data\\M.ICD");

    std::cout << std::fixed << std::setprecision(15);
    std::cout << "start_pk=" << fu.start_pk << "  end_pk=" << fu.end_pk << "\n\n";

    double pks[] = {2147.474, 2192.474, 2237.474, 2282.474,
                    2327.474, 2372.474, 2417.474, 2452.474};

    for (double pk : pks) {
        Vector d = fu.get_dir(pk);
        double ang = std::atan2(d.X(), d.Y());   // 方位角(从+Y北向起)
        Vector c = fu.get_coordinate(pk);
        std::cout << std::setprecision(3) << "pk=" << pk
                  << std::setprecision(15)
                  << "  ang=" << ang
                  << "  dir=(" << d.X() << ", " << d.Y() << ")"
                  << "  pt=(" << c.X() << ", " << c.Y() << ")\n";
    }
    return 0;
}
