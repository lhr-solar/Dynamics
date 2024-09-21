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
        print('Final Answer:',self.answer)




def main():
    p = [[125,80,100],[125,-80,100],[125,80,20],[125,-80,20],[45,0,150],[25,0,90],[20,0,10],[30,0,12],[0,0,0],[23,-40,70],[28,-120,70]]
    f = [-1000,0,0]
    a = Solver(p,f)
    a.unit_vector()
    a.summation_force_and_moment()
    a.final_calc()
main()
