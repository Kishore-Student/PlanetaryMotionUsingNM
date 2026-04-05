## Importing modules 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import NewtonMethod as NM
from scipy.interpolate import CubicSpline
import matplotlib.animation as animation

## IMPORTING DATASET
data=pd.read_csv("/home/kishore/Desktop/Numerical_Methods/Module2/Planet_data.csv",parse_dates=["date"])

## Separating the planet data from the dataset
last=687        ## Length of a MARTIAN year
Mercury=data.loc[data["name"]=="1 MERCURY BARYCENTER",["date", "x_au", "y_au"]].iloc[:last]
Venus=data.loc[data["name"]=="2 VENUS BARYCENTER",["date", "x_au", "y_au"]].iloc[:last]
Earth=data.loc[data["name"]=="3 EARTH BARYCENTER",["date", "x_au", "y_au"]].iloc[:last]
Mars=data.loc[data["name"]=="4 MARS BARYCENTER",["date", "x_au", "y_au"]].iloc[:last]
Jupyter=data.loc[data["name"]=="5 JUPITER BARYCENTER",["date", "x_au", "y_au"]].iloc[:last]
Saturn=data.loc[data["name"]=="6 SATURN BARYCENTER",["date", "x_au", "y_au"]].iloc[:last]
Uranus=data.loc[data["name"]=="7 URANUS BARYCENTER",["date", "x_au", "y_au"]].iloc[:last]
Neptune=data.loc[data["name"]=="8 NEPTUNE BARYCENTER",["date", "x_au", "y_au"]].iloc[:last]
## Grouping the planets
Planets={"Mercury":Mercury,"Venus":Venus,"Earth":Earth,"Mars":Mars,"Jupyter":Jupyter,"Saturn":Saturn,"Uranus":Uranus,"Neptune":Neptune}
for _,Planet in Planets.items():
    Planet["day"]=(Planet["date"]-Planet["date"].iloc[0]).dt.days  # Convert the dates to day counts

## Finding points using interpolation
## Creating a DataFrame to store values
PlanetEval=pd.DataFrame()
for name,Planet in Planets.items():
    ## Get samples
    samplesize=50
    x=Planet["x_au"].values[::samplesize]
    y=Planet["y_au"].values[::samplesize]
    day=Planet["day"].values[::samplesize]

    ## Get actual Positions
    xa=Planet["x_au"].values
    ya=Planet["y_au"].values
    
    ## Find difference table
    Tablex=NM.Table(day,x)
    Tabley=NM.Table(day,y)
    
    ## Perform interpolation
    Interpolated_x=NM.NewtonPolyMultiple(diff_table=Tablex,targets=Planet.day.values,x=day,mode="forward")
    Interpolated_y=NM.NewtonPolyMultiple(diff_table=Tabley,targets=Planet.day.values,x=day,mode="forward")
    CX=CubicSpline(day,x)
    CY=CubicSpline(day,y)
    C_x=CX(Planet.day.values)
    C_y=CY(Planet.day.values)
    ## Find errors for x and y positions
    errxN = np.where(xa != 0, (Interpolated_x - xa) / xa, 0)
    erryN = np.where(ya != 0, (Interpolated_y - ya) / ya, 0)
    errxC = np.where(xa != 0, (C_x- xa) / xa, 0)
    erryC= np.where(ya != 0, (C_y - ya) / ya, 0)
    PlanetEval[f"{name}_xN"]=pd.Series(Interpolated_x)
    PlanetEval[f"{name}_yN"]=pd.Series(Interpolated_y)
    PlanetEval[f"{name}_xC"]=C_x
    PlanetEval[f"{name}_yC"]=C_y
    PlanetEval[f"{name}_errxN"]=pd.Series(errxN)
    PlanetEval[f"{name}_erryN"]=pd.Series(erryN)
    PlanetEval[f"{name}_errxC"]=errxC
    PlanetEval[f"{name}_erryC"]=erryC

## Animation using matplotlib
fig, (axis1, axis2) = plt.subplots(1, 2)
## Create 4 planet's curves using interpolated data
##mercury,=axis1.plot([],[],"--",color="gray")
venus,=axis1.plot([],[],"--",color="orange",label="venus")
earth,=axis1.plot([],[],"--",color="blue",label="earth")
mars,=axis1.plot([],[],"--",color="red",label="mars")
sun=axis1.plot(0,0,'yo',markersize=20)

## Create 4 planet's curves using actual data
# ACTUAL (axis2)
venus_r, = axis2.plot([], [], color="orange",label="venus")
earth_r, = axis2.plot([], [], color="blue",label="earth")
mars_r, = axis2.plot([], [], color="red",label="mars")
venus_dot_r, = axis2.plot([], [], 'o', color="orange")
earth_dot_r, = axis2.plot([], [], 'o', color="blue")
mars_dot_r, = axis2.plot([], [], 'o', color="red")
axis2.plot(0, 0, 'yo', markersize=20)

##mercury_dot,=axis1.plot([],[],'o',color="gray")
venus_dot,=axis1.plot([],[],'o',color="orange")
earth_dot,=axis1.plot([],[],'o',color="blue")
mars_dot,=axis1.plot([],[],'o',color="red")
for ax in (axis1, axis2):
    ax.set_xlim(PlanetEval["Earth_xN"].min()-2, PlanetEval["Earth_xN"].max()+2)
    ax.set_ylim(PlanetEval["Earth_yN"].min()-2, PlanetEval["Earth_yN"].max()+2)
    ax.legend()
    ax.set_aspect('equal')

axis1.set_title("Interpolated (Newton)")
axis2.set_title("Actual Orbit")
def update(frame):
    # Plotting interpolated values
#___________________VENUS_______________________
    xv = PlanetEval["Venus_xN"].values[:frame]
    yv = PlanetEval["Venus_yN"].values[:frame]
#___________________EARTH_______________________
    xe = PlanetEval["Earth_xN"].values[:frame]
    ye = PlanetEval["Earth_yN"].values[:frame]
#___________________MARS_______________________
    xM = PlanetEval["Mars_xN"].values[:frame]
    yM = PlanetEval["Mars_yN"].values[:frame]

    venus.set_data(xv, yv)
    earth.set_data(xe, ye)
    mars.set_data(xM, yM)

    # Curves for Actual data
#___________________VENUS_______________________
    xv_r = Planets["Venus"]["x_au"].values[:frame]
    yv_r = Planets["Venus"]["y_au"].values[:frame]
#___________________EARTH_______________________
    xe_r = Planets["Earth"]["x_au"].values[:frame]
    ye_r = Planets["Earth"]["y_au"].values[:frame]
#___________________MARS_______________________
    xM_r = Planets["Mars"]["x_au"].values[:frame]
    yM_r = Planets["Mars"]["y_au"].values[:frame]

    venus_r.set_data(xv_r, yv_r)
    earth_r.set_data(xe_r, ye_r)
    mars_r.set_data(xM_r, yM_r)

    if frame > 0:
        venus_dot.set_data([xv[-1]], [yv[-1]])
        earth_dot.set_data([xe[-1]], [ye[-1]])
        mars_dot.set_data([xM[-1]], [yM[-1]])

        venus_dot_r.set_data([xv_r[-1]], [yv_r[-1]])
        earth_dot_r.set_data([xe_r[-1]], [ye_r[-1]])
        mars_dot_r.set_data([xM_r[-1]], [yM_r[-1]])

    return (
        venus, venus_dot,
        earth, earth_dot,
        mars, mars_dot,
        venus_r, venus_dot_r,
        earth_r, earth_dot_r,
        mars_r, mars_dot_r
    )

ani=animation.FuncAnimation(fig,update,frames=len(PlanetEval["Earth_xN"]),interval=20,blit=True)
plt.show()



