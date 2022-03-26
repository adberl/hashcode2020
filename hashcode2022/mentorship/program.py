inputs = {
    "a":"input_data/a_an_example.in.txt", 
    "b":"input_data/b_better_start_small.in.txt",
    "c":"input_data/c_collaboration.in.txt",
    "d":"input_data/d_dense_schedule.in.txt",
    "e":"input_data/e_exceptional_skills.in.txt",
    "f":"input_data/f_find_great_mentors.in.txt",
}

class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
        self.occupied = False
        self.working_on = None

    def __str__(self):
        ret_str = f"Contributor {str(hash(self))} | Name: {self.name} | Skills: {self.skills}"
        return ret_str
		
    def __repr__(self):
        return self.__str__()# + "\n"

class Project:
    def __init__(self, name, duration, score, best_before, roles):
        self.name = name
        self.duration = duration
        self.score = score
        self.best_before = best_before
        self.roles = roles
        self.progress = 0
        self.contributors_working = []
        self.filled_roles = {}

    def step(self, day):
        self.progress += 1
        if self.progress == self.duration:
            print(f"finished project {self.name} in {day} using {self.contributors_working}")
            for c, r in self.contributors_working:
                if r in c.skills:
                    print(f"{c.name} has increased {r} to level {c.skills[r] + 1}")
                    c.skills[r] += 1
                    c.occupied = False
            return True
        return False

    def start(self):
        print(f"Trying to start project {self.name} with {self.filled_roles}")
        tmp_working = []
        for r in self.filled_roles:
            for c in self.filled_roles[r]:
                if c[1] == False and not c[0].occupied: # doesnt need a mentor
                    tmp_working.append((c[0], r))
                    break

        if len(tmp_working) == len(self.roles):
            for c in tmp_working:
                c[0].occupied = True
                self.contributors_working.append(c)
            print(f"Started project {self.name} with {self.contributors_working} working on {self.roles}")
            return True
        return False

    def fill_roles(self, contributor):
        roles = self.roles
        for role in roles:
            for skill in contributor.skills:
                # print("AAAA", role, skill)
                if role == skill and roles[role] <= contributor.skills[skill] + 1:
#                    print("BBBB", role, skill)
                    needs_mentor = False
                    if contributor.skills[skill] + 1 == roles[role]:
                        needs_mentor = True
                    if role in self.filled_roles:
                        self.filled_roles[role].append((contributor, needs_mentor))
                    else:
                        self.filled_roles[role] = [(contributor, needs_mentor)]
 #                   print(self.filled_roles[role])

    def clear_fill(self):  
        for role in self.filled_roles:
            self.filled_roles[role] = []
    #def fill_mentors(self):
    #    for role in filled_roles:
    #        for relationship in filled_roles

    def __str__(self):
        ret_str = f"Project {self.name} | Duration: {self.duration} | Score: {self.score} | Best before: {self.best_before} | Roles: {self.roles} | Filled roles: {self.filled_roles}"
        return ret_str
		
    def __repr__(self):
        return self.__str__() + "\n"

def read_contributors(n, lines):
    contributors = []
    for _ in range(n):
        skills_dict = {}
        name, skills_n = lines.pop(0).split(" ")
        for _ in range(int(skills_n)):
            skill_name, skill_level = lines.pop(0).split(" ")
            skills_dict[skill_name] = int(skill_level)
        contributors.append(Contributor(name, skills_dict))
    return contributors, lines

def read_projects(n, lines):
    projects = []
    for _ in range(n):
        name, duration, score, best_before, skills_n = lines.pop(0).split(" ")
        roles_dict = {}
        for _ in range(int(skills_n)):
            skill_name, skill_level = lines.pop(0).split(" ")
            roles_dict[skill_name] = int(skill_level)
        projects.append(Project(name, int(duration), int(score), int(best_before), roles_dict))
    return projects

def read_file(file):
    input_data = inputs[file]
    all_lines = [i.rstrip() for i in open(input_data, 'r').readlines()]
    contr_n, proj_n =  [int(i) for i in all_lines.pop(0).split(" ")]
    print(f"contributors: {contr_n}, projects: {proj_n}")
    all_contributors, all_lines = read_contributors(contr_n, all_lines)
    all_projects = read_projects(proj_n, all_lines)
#    print(all_contributors)
#    print(all_projects)
    return all_contributors, all_projects

def main():
    day = 0
    done_projects = []
    file_name = "b"
    all_contributors, all_projects = read_file(file_name)
    ongoing_projects = []
    for p in all_projects:
        p.clear_fill()
        for c in all_contributors:
            p.fill_roles(c)
    for project in all_projects:
        if project.start():
            ongoing_projects.append(project)
            all_projects.remove(project)
    for p in ongoing_projects:
        if p in all_projects:
            all_projects.remove(p)
    #print(ongoing_projects)
    while True:
        day += 1
        needs_refill = False
        to_remove = []
        for p in ongoing_projects: 
            if p.step(day): # THIS IS WHERE A PROJECT ENDS
#                print(f"finished project {p.name} in {day} using {p.contributors_working}")
                needs_refill = True
                to_remove.append(p)
                working_list = [(c[0].name, c[1]) for c in p.contributors_working]                
                done_projects.append((p, working_list))
                
        for g in to_remove:
            ongoing_projects.remove(g)

        if needs_refill:
            #print(all_projects)
            for p in all_projects:
                p.clear_fill()
                for c in all_contributors:
                    p.fill_roles(c)
            for project in all_projects:
                if project.start():
                    ongoing_projects.append(project)
            for p in ongoing_projects:
                if p in all_projects:
                    all_projects.remove(p)

        if len(ongoing_projects) == 0: #.empty():
            break

    # LIST OF PEOPLE WORKING NEEDS TO BE REVERSED
    output = open(f"output_{file_name}.txt", "w")
    output.write(str(len(done_projects)) + "\n")
    for p in done_projects:
        output.write(p[0].name + "\n")
        w = ""
        for r in p[0].roles:
            for c in p[1]:
                if c[1] == r:
                    w +=  c[0] + " "
                    break
        output.write(w.rstrip() + "\n")
    output.close()
    print(done_projects)
 #   print(all_projects)










if __name__ == "__main__":
    main()