import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl

class fuzzy_controller(object):
    #输入五个论域的范围，为np.array的格式
    #names=['nb','nm','ns','z','ps','pm','pb']
    def __init__(self,universe_fx,universe_dfx,universe_kp,universe_ki,universe_kd,name1,name2,names):
        self.warn=False
        # self.limit=limit
        self.u_f = universe_fx
        self.u_df = universe_dfx
        self.u_kp = universe_kp
        self.u_ki = universe_ki
        self.u_kd = universe_kd
        self.names=names
        self.name1=name1
        self.name2=name2
        self.f=ctrl.Antecedent(self.u_f,self.name1)
        self.df=ctrl.Antecedent(self.u_df,self.name2)
        self.kp=ctrl.Consequent(self.u_kp,'kp')
        self.ki=ctrl.Consequent(self.u_ki,'ki')
        self.kd=ctrl.Consequent(self.u_kd,'kd')

        self.f.automf(7,names=self.names)
        self.df.automf(7,names=self.names)
        self.kp.automf(7,names=self.names)
        self.ki.automf(7,names=self.names)
        self.kd.automf(7,names=self.names)
        # self.f.view()
        # self.kp.view()
        # self.df.view()
        # self.ki.view()
        # self.kd.view()

        self.rule=[]
        #1
        # self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['nb']), consequent=(self.kp['pb'] ,self.ki['nb'] , self.kd['ps']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['nb']), consequent=(self.kp['pb'] , self.ki['nb'] , self.kd['ps']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['nb']), consequent=(self.kp['pm'] , self.ki['nb'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['nb']), consequent=(self.kp['pm'] , self.ki['nm'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['nb']), consequent=(self.kp['ps'] , self.ki['nm'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['nb']), consequent=(self.kp['ps'] , self.ki['z'] , self.kd['pb']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['nb']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['pb']))]
        # #2
        # self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['nm']), consequent=(self.kp['pb'] , self.ki['nb'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['nm']), consequent=(self.kp['pb'] , self.ki['nb'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['nm']), consequent=(self.kp['pm'] , self.ki['nm'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['nm']), consequent=(self.kp['pm'] , self.ki['nm'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['nm']), consequent=(self.kp['ps'] , self.ki['ns'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['nm']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['nm']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['pm']))]
        # #3
        # self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['ns']), consequent=(self.kp['pm'] , self.ki['nm'] , self.kd['nb']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['ns']), consequent=(self.kp['pm'] , self.ki['nm'] , self.kd['nb']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['ns']), consequent=(self.kp['pm'] , self.ki['ns'] , self.kd['nm']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['ns']), consequent=(self.kp['ps'] , self.ki['ns'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['ns']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['ns']), consequent=(self.kp['ns'] , self.ki['ps'] , self.kd['ps']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['ns']), consequent=(self.kp['pm'] , self.ki['ps'] , self.kd['pm']))]#改
        # #4
        # self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['z']), consequent=(self.kp['pm'] , self.ki['nm'] , self.kd['nb']))]#改
        # self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['z']), consequent=(self.kp['ps'] , self.ki['ns'] , self.kd['nm']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['z']), consequent=(self.kp['ps'] , self.ki['ns'] , self.kd['nm']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['z']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['z']), consequent=(self.kp['ns'] , self.ki['ps'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['z']), consequent=(self.kp['nm'] , self.ki['ps'] , self.kd['ps']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['z']), consequent=(self.kp['pm'] , self.ki['pm'] , self.kd['pm']))]
        # #5
        # self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['ps']), consequent=(self.kp['ps'] ,self.ki['ns'] , self.kd['nb']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['ps']), consequent=(self.kp['ps'] , self.ki['ns'] , self.kd['nm']))]
        # self.rule+= [ctrl.Rule(antecedent=(self.f['ns'] & self.df['ps']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['ps']), consequent=(self.kp['ns'] , self.ki['ps'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['ps']), consequent=(self.kp['ns'] , self.ki['ps'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['ps']), consequent=(self.kp['nm'] , self.ki['pm'] , self.kd['ps']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['ps']), consequent=(self.kp['nm'] , self.ki['pm'] ,self.kd['ps']))]
        # #6
        # self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['pm']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['nm']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['pm']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['pm']), consequent=(self.kp['ns'] , self.ki['ps'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['pm']), consequent=(self.kp['nm'] , self.ki['pm'] , self.kd['ns']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['pm']), consequent=(self.kp['nm'] , self.ki['pm'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['pm']), consequent=(self.kp['nm'] , self.ki['pb'] , self.kd['ps']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['pm']), consequent=(self.kp['nb'] , self.ki['pb'] , self.kd['ps']))]
        # #7
        # self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['pb']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['ps']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['pb']), consequent=(self.kp['ns'] , self.ki['z'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['pb']), consequent=(self.kp['ns'] , self.ki['ps'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['pb']), consequent=(self.kp['nm'] , self.ki['pm'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['pb']), consequent=(self.kp['nm'] , self.ki['pb'] , self.kd['z']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['pb']), consequent=(self.kp['nb'] , self.ki['pb'] , self.kd['pb']))]
        # self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['pb']), consequent=(self.kp['nb'] , self.ki['pb'] , self.kd['pb']))]
        # ctrl.Rule(antecedent=(self.f['nb'] & self.df['nb']), consequent=(self.kp['pb'], self.ki['nb'], self.kd['ps'])).view()
        self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['nb']), consequent=(self.kp['pb'] ,self.ki['pb'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['nb']), consequent=(self.kp['pb'] , self.ki['pb'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['nb']), consequent=(self.kp['pb'] , self.ki['pm'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['nb']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['z']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['nb']), consequent=(self.kp['nb'] , self.ki['ps'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['nb']), consequent=(self.kp['nm'] , self.ki['pm'] , self.kd['pm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['nb']), consequent=(self.kp['ns'] , self.ki['pb'] , self.kd['ns']))]
        #2
        self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['nm']), consequent=(self.kp['pb'] , self.ki['pb'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['nm']), consequent=(self.kp['pb'] , self.ki['pm'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['nm']), consequent=(self.kp['pm'] , self.ki['ps'] , self.kd['pm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['nm']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['z']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['nm']), consequent=(self.kp['nm'] , self.ki['nb'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['nm']), consequent=(self.kp['ns'] , self.ki['nb'] , self.kd['ps']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['nm']), consequent=(self.kp['z'] , self.ki['nm'] , self.kd['nm']))]
        #3
        self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['ns']), consequent=(self.kp['pb'] , self.ki['pb'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['ns']), consequent=(self.kp['pm'] , self.ki['pm'] , self.kd['pm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['ns']), consequent=(self.kp['pm'] , self.ki['ps'] , self.kd['pm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['ns']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['z']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['ns']), consequent=(self.kp['ns'] , self.ki['nb'] , self.kd['pm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['ns']), consequent=(self.kp['z'] , self.ki['nm'] , self.kd['z']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['ns']), consequent=(self.kp['ps'] , self.ki['ns'] , self.kd['nb']))]#改
        #4
        self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['z']), consequent=(self.kp['pb'] , self.ki['pb'] , self.kd['nb']))]#改
        self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['z']), consequent=(self.kp['pm'] , self.ki['pm'] , self.kd['nm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['z']), consequent=(self.kp['ps'] , self.ki['ps'] , self.kd['ns']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['z']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['z']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['z']), consequent=(self.kp['ps'] , self.ki['ps'] , self.kd['ns']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['z']), consequent=(self.kp['pm'] , self.ki['pm'] , self.kd['nm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['z']), consequent=(self.kp['pb'] , self.ki['pb'] , self.kd['nb']))]
        #5
        self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['ps']), consequent=(self.kp['ps'] ,self.ki['ns'] , self.kd['nb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['ps']), consequent=(self.kp['z'] , self.ki['nm'] , self.kd['z']))]
        self.rule+= [ctrl.Rule(antecedent=(self.f['ns'] & self.df['ps']), consequent=(self.kp['ns'] , self.ki['nb'] , self.kd['pm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['ps']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['z']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['ps']), consequent=(self.kp['pm'] , self.ki['ps'] , self.kd['pm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['ps']), consequent=(self.kp['pb'] , self.ki['pm'] , self.kd['pm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['ps']), consequent=(self.kp['pb'] , self.ki['pb'] ,self.kd['pb']))]
        #6
        self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['pm']), consequent=(self.kp['z'] , self.ki['nm'] , self.kd['nm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['pm']), consequent=(self.kp['ns'] , self.ki['nb'] , self.kd['ps']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['pm']), consequent=(self.kp['nm'] , self.ki['nb'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['pm']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['z']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['pm']), consequent=(self.kp['pm'] , self.ki['pm'] , self.kd['pm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['pm']), consequent=(self.kp['pb'] , self.ki['pb'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['pm']), consequent=(self.kp['pb'] , self.ki['pb'] , self.kd['pb']))]
        #7
        self.rule += [ctrl.Rule(antecedent=(self.f['nb'] & self.df['pb']), consequent=(self.kp['ns'] , self.ki['nb'] , self.kd['ns']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['nm'] & self.df['pb']), consequent=(self.kp['nm'] , self.ki['nb'] , self.kd['pm']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ns'] & self.df['pb']), consequent=(self.kp['nb'] , self.ki['nb'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['z'] & self.df['pb']), consequent=(self.kp['z'] , self.ki['z'] , self.kd['z']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['ps'] & self.df['pb']), consequent=(self.kp['pb'] , self.ki['pb'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pm'] & self.df['pb']), consequent=(self.kp['pb'] , self.ki['pb'] , self.kd['pb']))]
        self.rule += [ctrl.Rule(antecedent=(self.f['pb'] & self.df['pb']), consequent=(self.kp['pb'] , self.ki['pb'] , self.kd['pb']))]
        self.system=ctrl.ControlSystem(rules=self.rule)

    def output(self,f,df):
        cal_output=ctrl.ControlSystemSimulation(self.system)
        cal_output.input[self.name1]=f
        cal_output.input[self.name2]=df
        cal_output.compute()
        self.dict={}
        self.dict['kp']=cal_output.output['kp']
        self.dict['ki']=cal_output.output['ki']
        self.dict['kd']=cal_output.output['kd']
        # if (abs(f)>=self.limit):
        #     self.warn=True
        return self.dict['kp'],self.dict['ki'],self.dict['kd']
if '__name__'=='__main__':
    a=fuzzy_controller(np.arange(-10,10.5,0.5),np.arange(-10,10.5,0.5),np.arange(-0.5,0.56,0.01),np.arange(-1,1.1,0.1),np.arange(-1,1.1,0.1),'fy',
                                                 'dfy',['nb','nm','ns','z','ps','pm','pb'])
    a.kp.view()




