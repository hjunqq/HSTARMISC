from enum import Enum

from gpro.helper import isint


class Component(Enum):
    Displacement = 0
    Tofor = 1
    Stress = 2
    PrincipleStress = 3
    Damage = 4
    InternalForce = 5


class SingleResult:
    def __init__(self, index, value):
        self.index = index
        self.value = value


class ResultSet:
    displacement = []
    tofor = []
    stress = []
    principle = []
    damage = []
    internalforce = []
    component = {}
    time = 0.0

    def __init__(self, time):
        self.time = time
        self.displacement = []
        self.tofor = []
        self.stress = []
        self.principle = []
        self.damage = []
        self.internalforce = []

    def append(self, result, dest):
        if dest == 0:
            self.displacement.append(result)
        elif dest == 1:
            self.tofor.append(result)
        elif dest == 2:
            self.stress.append(result)
        elif dest == 3:
            self.principle.append(result)
        elif dest == 4:
            self.damage.append(result)
        elif dest == 5:
            self.internalforce.append(result)

    def get_time(self):
        return self.time

    def get_value(self, dest):
        if dest == 0:
            return self.displacement
        elif dest == 1:
            return self.tofor
        elif dest == 2:
            return self.stress
        elif dest == 3:
            return self.principle
        elif dest == 4:
            return self.damage
        elif dest ==5:
            return self.internalforce


class Result:
    """ gid res """

    def __init__(self, file_path):
        self.file_path = file_path
        self.n_step = 0
        self.n_res = 0
        self.res_set = []
        self.res = None

    def read(self):
        step_time = 0.0
        with open(self.file_path, 'r') as f:
            for line in f:
                vals = line.split()
                new_res = False
                # 判断结果分组
                if vals[0].lower() == "displacement":
                    dest = 0
                    current_time = float(vals[2])
                elif vals[0].lower() == "tofor":
                    dest = 1
                    current_time = float(vals[2])
                elif vals[0].lower() == "stress":
                    dest = 2
                    current_time = float(vals[2])
                elif vals[0].lower() == "principalstress":
                    dest = 3
                    current_time = float(vals[2])
                elif vals[0].lower() == "yield":
                    dest = 4
                    current_time = float(vals[2])
                elif vals[0].lower() == "internal_force_":
                    dest = 5
                    current_time = float(vals[2])

                if current_time != step_time:
                    if self.res is not None:
                        self.res_set.append(self.res)
                    self.res = ResultSet(current_time)
                    self.n_step += 1
                    step_time = current_time
                # 补充结果
                if isint(vals[0]):
                    result = SingleResult(int(vals[0]), list(map(float, vals[1:])))
                    self.res.append(result, dest)

        self.res_set.append(self.res)

        print("len:", len(self.res_set))

    def get_time_series(self, point, comp_index):
        if self.n_step <= 0:
            print("还没有读取结果！")
            return
        time_series = []
        value_series = []
        for ires in self.res_set:
            time_series.append(ires.get_time())
            for ival in ires.get_value(comp_index):
                if ival.index == point:
                    value_series.append(ival.value)

        print(len(time_series))

        return time_series, value_series

    def get_value(self,point, comp_index,istep):
        if self.n_step <= 0:
            print("还没有读取结果！")
            return

        time = 0
        value = []
        ires = self.res_set[istep]
        for ival in ires.get_value(comp_index):
            time = ires.get_time()
            if ival.index == point:
                value = ival.value

        return time,value

    def get_all_value_by_time(self,comp_index,istep):
        if self.n_step <= 0:
            print("还没有读取结果！")
            return
        ires = self.res_set[istep]
        time = ires.get_time()
        val = ires.get_value(comp_index)
        return val


