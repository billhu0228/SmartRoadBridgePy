#include <locale>
#include <codecvt>
#include <string>
#include <sstream>
#include "PQX.h"
#include "PQXElement.h"
#include "Straight.h"
#include "Arc.h"
#include "Sprial.h"
#include "base.h"

using namespace std;

//std::wstring ToUtf16(std::string str) {
//    std::wstring ret;
//    int len = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), str.length(), NULL, 0);
//    if (len > 0) {
//        ret.resize(len);
//        MultiByteToWideChar(CP_UTF8, 0, str.c_str(), str.length(), &ret[0], len);
//    }
//    return ret;
//}

PQX::PQX(void) {
    start_pk = 0;
    start_point = Vector();
    start_angle = Angle();
    end_pk = 0;

}

PQX::PQX(std::wstring filepath) {
    start_pk = 0;
    start_point = Vector();
    start_angle = Angle();
    Vector cur_point = Vector(0, 0);
    Angle cur_angle = Angle(Degree(0));
    string t1;
    vector<wstring> text;


    std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;

    fstream fid;
    fid.open(filepath, std::ofstream::in);

    while (getline(fid, t1)) {
        std::wstring wide = converter.from_bytes(t1);
        text.push_back(wide);
    }
    fid.close();
    std::wstringstream ss;
    for (size_t i = 0; i < text.size(); ++i) {
        if (i != 0)
            ss << L"\n";
        ss << text[i];
    }
    PQX::ICDText = ss.str();

    wstring line;

    for (size_t i = 0; i < text.size(); i++) {
        line = text[i];

        if (i == 0) {
            start_pk = stod(line);
        } else if (i == 1) {
            vector<string> xx;
            boost::split(xx, line, boost::is_any_of(","), boost::token_compress_on);
            double start_x = stod(xx[0]);
            double start_y = stod(xx[1]);
            double start_ang_in_rad = stod(xx[2]);
            start_point = Vector(start_y, start_x);
            start_angle = Angle(Degree(start_ang_in_rad / Angle::PI * 180.0));
            cur_point = start_point;
            cur_angle = start_angle;
        } else {
            vector<string> xx;
            boost::split(xx, line, boost::is_any_of(","), boost::token_compress_on);
            if (line.substr(0, 2) == L"//") {
                continue;
            } else if (xx.size() == 3 && stoi(xx[2]) == 0) {
                break;
            } else {
                PQXElement *item = nullptr;
                Straight str;
                Sprial spr;
                Arc arc;
                int type_id = stoi(xx[0]);
                double aa, ll, st_r, end_r, rr;
                LeftRightEnum lr_dir;
                EITypeID idd;
                switch (type_id) {
                    case 1:
                        ll = stod(xx[1]);
                        // 补充考虑突变夹角
                        if (xx.size() == 3) {
                            cur_angle = stod(xx[2]);
                        }
                        item = new Straight(ll, cur_point, cur_angle);
                        break;
                    case 2:
                        rr = stod(xx[1]);
                        ll = stod(xx[2]);
                        lr_dir = LeftRightEnum(stoi(xx[3]));
                        // 补充考虑突变夹角
                        if (xx.size() == 5) {
                            cur_angle = stod(xx[4]);
                        }
                        item = new Arc(rr, ll, cur_point, cur_angle, lr_dir);
                        break;
                    case 3:
                        idd = EITypeID(type_id);
                        aa = stod(xx[1]);
                        end_r = stod(xx[2]);
                        lr_dir = LeftRightEnum(stoi(xx[3]));
                        item = new Sprial(idd, aa, 1e39, end_r, cur_point, cur_angle, lr_dir);
                        break;
                    case 4:
                        idd = EITypeID(type_id);
                        aa = stod(xx[1]);
                        st_r = stod(xx[2]);
                        lr_dir = LeftRightEnum(stoi(xx[3]));
                        item = new Sprial(idd, aa, st_r, 1e39, cur_point, cur_angle, lr_dir);
                        break;
                    case 5:
                    case 6:
                        idd = EITypeID(type_id);
                        aa = stod(xx[1]);
                        st_r = stod(xx[2]);
                        end_r = stod(xx[3]);
                        lr_dir = LeftRightEnum(stoi(xx[4]));
                        item = new Sprial(idd, aa, st_r, end_r, cur_point, cur_angle, lr_dir);
                        // 怀疑构造函数的终点半径输入错误；
                        break;
                    default:
                        throw exception("读取ICD文件错误.");
                        break;
                }

                elem_collection.push_back(item);
                cur_angle = elem_collection.back()->end_angle();
                cur_point = elem_collection.back()->end_point();;
            }


        }

    }

    end_pk = __get_end_pk();

}

double PQX::__get_end_pk() const {
    if (elem_collection.size() == 0) {
        return start_pk;
    } else {
        double totalLength = 0;
        for (auto l :elem_collection) {
            totalLength = totalLength + l->length();
        }
        return start_pk + totalLength;
    }
}

Vector PQX::get_coordinate(double pk) const {
    if (pk < start_pk) {
        return get_coordinate(start_pk);
    } else if (pk <= end_pk) {
        vector<double> tmp;
        for (auto item :elem_collection) {
            tmp.push_back(item->length());
        }
        vector<double> len_sum_up = {start_pk};
        for (auto ll : tmp) {
            len_sum_up.push_back(len_sum_up.back() + ll);
        }
        int aa = 0;
        for (aa = 0; aa < len_sum_up.size(); aa++)// 要注意这里aa和enumerate的区别
        {
            double val = len_sum_up[aa];
            if (val > pk) {
                break;
            }
        }
        if (aa == len_sum_up.size()) {
            aa = aa - 1;
        }
        aa = aa - 1;
        double pre_pk;
        if (pk == end_pk) {
            pre_pk = len_sum_up[len_sum_up.size() - 2];
        } else {
            pre_pk = len_sum_up[aa];
        }
        double ll = pk - pre_pk;
        auto res = (elem_collection[aa])->get_point_on_curve(ll);
        return res;
    }
    return Vector();
}

Vector PQX::get_dir(double pk, double delta) const {
    double x0, y0, x1, y1, ll;
    if (pk == end_pk) {
        x0 = get_coordinate(pk - delta).X();
        y0 = get_coordinate(pk - delta).Y();
        x1 = get_coordinate(pk).X();
        y1 = get_coordinate(pk).Y();
    } else if (pk == start_pk) {
        x0 = get_coordinate(pk).X();
        y0 = get_coordinate(pk).Y();
        x1 = get_coordinate(pk + delta).X();
        y1 = get_coordinate(pk + delta).Y();
    } else {
        x0 = get_coordinate(pk - delta).X();
        y0 = get_coordinate(pk - delta).Y();
        x1 = get_coordinate(pk + delta).X();
        y1 = get_coordinate(pk + delta).Y();
    }
    ll = sqrt((x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1));
    return Vector((x1 - x0) / ll, (y1 - y0) / ll);
}

double PQX::get_station_by_point(double x0, double y0, int step, double delta) {
    vector<pair<double, double>> res;
    double k0err[2];
    double dk = (end_pk - start_pk) / step;
    Vector target = Vector(x0, y0);
    double k1, k2;
    for (int i = 0; i < step; i++) {
        k1 = start_pk + dk * i;
        k2 = k1 + dk;
        __binary_test__(k1, k2, target, delta, k0err);
        res.push_back(pair<double, double>{k0err[0], k0err[1]});
    }
    sort(res.begin(), res.end(),
         [](pair<double, double> a, pair<double, double> b) -> bool { return (a.second < b.second); });

    return res[0].first;
}


double PQX::get_station_by_point2(double x0, double y0, double x1, double y1, double delta) {
    Vector pt0 = Vector(x0, y0);
    Vector pt1 = Vector(x1, y1);
    double ret[2] = {start_pk, end_pk};
    while (ret[1] - ret[0] > delta) {
        __solve_coincidence(pt0, pt1, ret);
    }
    return (ret[0] + ret[1]) * 0.5;
}


int PQX::get_side(double x0, double y0) {
    double pk_center = get_station_by_point(x0, y0);
    Vector center = get_coordinate(pk_center);
    Vector v_dir = get_dir(pk_center);
    Vector v_cross = Vector(x0, y0) - center;
    if (v_cross.length() == 0) {
        return 0;
    } else {
        Angle ang = Angle(v_dir.angle_signed(v_cross));
        if (ang.GetDegree() < 0) {
            return 1;
        } else {
            return -1;
        }
    }
    return 0;
}

void PQX::__solve_closer(const Vector &pt, double ret[3]) {
    double pk1 = ret[0];
    double pk2 = ret[1];
    assert(pk1 <= pk2);
    Vector p1 = get_coordinate(pk1);
    Vector p2;
    // 修改了因pk2超过endpk造成的错误 -bill 10.15
    // Vector p2 = get_coordinate(pk2);
    if (abs(pk2 - end_pk) < 1.0e-6) {
        p2 = get_coordinate(end_pk);
    } else {
        p2 = get_coordinate(pk2);
    }
    if (p1.distance_point(pt) < p2.distance_point(pt)) {
        ret[0] = pk1;
        ret[1] = 0.5 * (pk1 + pk2);
        ret[2] = p1.distance_point(pt);
    } else {
        ret[0] = 0.5 * (pk1 + pk2);
        ret[1] = pk2;
        ret[2] = p2.distance_point(pt);
    }
}


/// 二分求解
/// \param pk1
/// \param pk2
/// \param pt
/// \param delta
/// \param ret 返回值分别为最优解及误差.
void PQX::__binary_test__(double pk1, double pk2, const Vector &pt, double delta, double ret[2]) {
    double mid = 0;
    double inputs[3] = {pk1, pk2, 0};
    while (abs(inputs[1] - inputs[0]) > delta) {
        __solve_closer(pt, inputs);
        mid = 0.5 * (inputs[0] + inputs[1]);
    }
    double res1 = mid;
    inputs[0] = res1;
    inputs[1] = res1;
    __solve_closer(pt, inputs);
    ret[0] = res1;
    ret[1] = inputs[2];
}


/// 求解与pt0,pt1 共线的点.
/// \param pt0
/// \param pt1
/// \param ret [k0,k1]
void PQX::__solve_coincidence(const Vector &pt0, const Vector &pt1, double *ret) {
    Vector dir = pt1 - pt0;
    assert(ret[1] > ret[0]);
    double km=(ret[0] + ret[1]) * 0.5;
    Vector v0 = get_coordinate(ret[0]) - pt0;
    Vector v1 = get_coordinate(ret[1]) - pt0;
    Vector vm = get_coordinate(km) - pt0;
    double ang0 = dir.angle_signed(v0);
    double ang1 = dir.angle_signed(v1);
    double ang_m = dir.angle_signed(vm);
    if (ang0 * ang1 > 0) {
        // 同向，反射
        double dl = ret[1] - ret[0];
        if (abs(ang0) < abs(ang1)) {
            ret[1] = ret[0];
            ret[0] = ret[0] - dl;
        } else {
            ret[0] = ret[1];
            ret[1] = ret[1] + dl;
        }

    } else {
        // 不同向，二分
        if (ang0 * ang_m > 0) {
            ret[0] = km;
        } else {
            ret[1] = km;
        }
    }
}


