import numpy as np

class Solver():
    def __init__(self,points,forces):
        self.points = np.array(points)
        self.forces = forces


    def unit_vector(self):
        self.force_unit_vectors = []
        force_vectors = []
        for i in range(5):
            if i < 2:
                j = 5
            elif i < 4:
                j = 6
            else:
                j = 7
            force_vectors.append(np.subtract(self.points[i], self.points[j]))
        force_vectors.append(np.subtract(self.points[10], self.points[9]))
        for vector in force_vectors:
            self.force_unit_vectors.append(vector/np.linalg.norm(vector))

    def summation_force_and_moment(self):
        sum_force_x_y_z_axis = []
        sum_moment_x_y_z_axis = []
        moment_arm = []
        axis = np.array([[1,0,0],[0,1,0],[0,0,1]])
        for j in range(3):
            lst = []
            for force in self.force_unit_vectors:
                lst.append(force[j])
            sum_force_x_y_z_axis.append(lst)
        for i in range(6):
            if i > 4:
                i += 5
            moment_arm.append(np.subtract(self.points[i],self.points[8]))
        for i in range(3):
            lst = []
            for j in range(len(self.force_unit_vectors)):
                lst.append(np.dot(axis[i],np.cross(moment_arm[j],self.force_unit_vectors[j])))
            sum_moment_x_y_z_axis.append(lst)
        self.matrix = np.array(sum_force_x_y_z_axis + sum_moment_x_y_z_axis)


    def final_calc(self):
        b = self.forces + [0,0,0]
        self.answer = np.linalg.solve(self.matrix,np.array(b))
        for j in range(len(self.answer)):
            print("F"+str(j+1)+" [N] :",self.answer[j])



def user_input():
    points = []
    forces = []
    for i in range(11):
        point = str(input("Enter the coordinates for each point in the form x,y,z: "))
        p = [float(x) for x in point.split(',')]
        points.append(p)
    Fcw = float(input("Enter the value for Fcw [N]: "))
    Fb = float(input("Enter the value for Fb [N]: "))
    Fn = float(input("Enter the value for Fn [N]: "))
    forces = [-Fcw,Fb,-Fn]
    a = Solver(points,forces)
    a.unit_vector()
    a.summation_force_and_moment()
    a.final_calc()
user_input()
