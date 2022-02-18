import meshio.med
import numpy as np

from gpro.Mesh import Mesh
from gpro.Result import Result


def cal_gap_width(s):
    msh_path = s + ".flavia.msh"
    msh = Mesh(msh_path)
    msh.read()

    cgroup = msh.group[2]
    first_four = []
    last_four = []
    for elemidx in cgroup.elements:
        elem = msh.element[elemidx - 1]
        first_four += elem.nodes[0:4]
        last_four += elem.nodes[4:8]

    first_four = np.unique(np.array(first_four))
    last_four = np.unique(np.array(last_four))
    n_point = len(first_four)

    cells = []
    for elemidx in cgroup.elements:
        elem = msh.element[elemidx - 1]
        enodes = []
        for idx in range(4):
            enodes += np.where(first_four == elem.nodes[idx])[0].tolist()
        cells.append(("quad", [enodes]))


    res_path = s + ".flavia.res"
    res = Result(res_path)
    res.read()

    disp = res.get_all_value_by_time(0, 99)
    disp_x = []
    disp_y = []
    disp_z = []
    for idisp in disp:
        disp_x.append(idisp.value[0])
        disp_y.append(idisp.value[1])
        disp_z.append(idisp.value[2])

    gap_x = []
    gap_y = []
    gap_z = []
    for first, last in zip(first_four, last_four):
        gap_x.append(disp_x[first - 1] - disp_x[last - 1])
        gap_y.append(disp_y[first - 1] - disp_y[last - 1])
        gap_z.append(disp_z[first - 1] - disp_z[last - 1])

    # write gap mesh
    points = []
    for idx in first_four:
        points.append(msh.node[idx - 1].coordinates)

    point_data = {'gap_x': gap_x, 'gap_y': gap_y, 'gap_z': gap_z}

    mesh = meshio.Mesh(points, cells, point_data)
    mesh.write("gap.plt", file_format="tecplot")


if __name__ == '__main__':
    cal_gap_width(r'G:\ZSJ\hstardebug (zz1109)\oblique_bolt\tunnel\4hstar\1')
