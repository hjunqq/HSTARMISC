from unittest import TestCase

from gpro.Mesh import Mesh
from gpro.Result import Result


class TestRes(TestCase):
    def test_read(self):
        file = r'G:\ZSJ\hstardebug (zz1109)\oblique_bolt\4hstar\1.flavia.res'
        res = Result(file)
        res.read()


class TestMesh(TestCase):
    def test_read(self):
        file = r'G:\ZSJ\hstardebug (zz1109)\oblique_bolt\4hstar\1.flavia.msh'
        mesh = Mesh(file)
        mesh.read()


class TestResult(TestCase):
    def test_get_time_series(self):
        file = r'G:\ZSJ\hstardebug (zz1109)\oblique_bolt\4hstar\1.flavia.res'
        res = Result(file)
        res.read()
        time,value = res.get_time_series(1,1)
        print(time,value)

class TestBemResult(TestCase):
    def test_get_time_series(self):
        file = r'G:\ZSJ\hstardebug (zz1109)\oblique_bolt\4hstar\1bem.flavia.res'
        res = Result(file)
        res.read()
        time,value = res.get_time_series(1,5)
        print(time,value)