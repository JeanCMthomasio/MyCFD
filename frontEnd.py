from nicegui import run, ui
import numpy as np
from matplotlib import cm


def DerivativeMatrix(u_filed, dt):
    N, M = u_filed.shape
    return np.eye(N*M, k= 0)/dt

def LaplacianMatrix(u_field, dx, dy):
    N, M  = u_field.shape
    laplacian = np.zeros(shape=(N*M, N*M))
    laplacian += np.eye(N*M, k= 0) * (-2 * (1/dx**2 + 1/dy**2))
    laplacian += np.eye(N*M, k= M) * (1/dx**2)
    laplacian += np.eye(N*M, k=-M) * (1/dx**2)
    laplacian += np.eye(N*M, k= 1) * (1/dy**2)
    laplacian += np.eye(N*M, k=-1) * (1/dy**2)
    return laplacian

def ConvectionMatrix(u_field, v_field, dx, dy):
    N, M  = u_field.shape
    u_vec = np.reshape(u_field, (N*M,))
    v_vec = np.reshape(v_field, (N*M,))
    convetion = np.zeros(shape=(N*M, N*M))
    convetion += np.diag( u_vec/dx) @ np.eye(N*M, k= M)
    convetion += np.diag(-u_vec/dx) @ np.eye(N*M, k= 0)
    convetion += np.diag( v_vec/dy) @ np.eye(N*M, k= 1)
    convetion += np.diag(-v_vec/dy) @ np.eye(N*M, k= 0)
    return convetion

def ApplyPressureBC(L, p_field):
    """Overwrite the boundary rows of a Laplacian operator with the pressure BCs:
       Neumann (zero-gradient) on the three walls, Dirichlet p=0 at the lid (pins p)."""
    N, M = p_field.shape
    i, j = np.divmod(np.arange(N*M), M)           # flat index -> (i,j)
    lid    =  j == M-1                            # top  (y max): Dirichlet p = 0
    bottom =  j == 0                              # bottom wall:  Neumann
    left   = (i == 0)   & (j > 0) & (j < M-1)     # left wall:    Neumann
    right  = (i == N-1) & (j > 0) & (j < M-1)     # right wall:   Neumann

    L = L.copy()
    L[lid | bottom | left | right, :] = 0.0       # clear boundary rows
    r = np.where(lid)[0];    L[r, r] = 1.0                    # p = 0
    r = np.where(bottom)[0]; L[r, r] = 1.0; L[r, r+1] = -1.0  # p = p[i,1]
    r = np.where(left)[0];   L[r, r] = 1.0; L[r, r+M] = -1.0  # p = p[1,j]
    r = np.where(right)[0];  L[r, r] = 1.0; L[r, r-M] = -1.0  # p = p[N-2,j]
    return L

def Simulation(configs):
    dx = 1/configs["N_CELLS_X"]
    dy = 1/configs["N_CELLS_Y"]
    dt = np.min([dx, dy]) * 1/configs["CFL"] / (1/configs["HORIZONTAL_VELOCITY_TOP"])

    # Linear spacing in points
    x = np.linspace(0.0, 1, configs["N_CELLS_X"]+1)
    y = np.linspace(0.0, 1, configs["N_CELLS_Y"]+1)

    # Domain Coordinates
    Y, X = np.meshgrid(y, x)

    # Initiate field template matrices 
    u_field = np.zeros_like(X)
    v_field = np.zeros_like(X)
    p_field = np.zeros_like(X)

    # Initial values
    t=0
    u_field_previous = u_field.copy()
    v_field_previous = v_field.copy()
    p_field_previous = p_field.copy()

    # Outer Time loop
    while t < configs["RUN_TIME"]:
        iter_step = 0
        print(f"Time:{t} s")

        # Calculate gradient of presuure
        dpdx, dpdy = np.gradient(p_field_previous, x, y)

        # Momentum Eq. Matrix Form
        # X direction
        Mu = (
            DerivativeMatrix(u_field_previous, dt) 
            + ConvectionMatrix(u_field_previous, v_field_previous, dx, dy) 
            - configs["KINEMATIC_VISCOSITY"] * LaplacianMatrix(u_field_previous, dx, dy)
        )
        Su = np.reshape(u_field_previous/dt - dpdx/configs["DENSITY"], shape=((configs["N_CELLS_X"] + 1)*(configs["N_CELLS_Y"] + 1),))
        u_tilde_next = np.linalg.solve(Mu, Su)

        # Y direction
        Mv = (
            DerivativeMatrix(v_field_previous, dt) 
            + ConvectionMatrix(u_field_previous, v_field_previous, dx, dy) 
            - configs["KINEMATIC_VISCOSITY"] * LaplacianMatrix(v_field_previous, dx, dy)
        )
        Sv = np.reshape(v_field_previous/dt - dpdy/configs["DENSITY"], shape=((configs["N_CELLS_X"] + 1)*(configs["N_CELLS_Y"] + 1),))
        v_tilde_next = np.linalg.solve(Mv, Sv)
        
        conv_criteria = False
        u_next = u_tilde_next.copy()
        v_next = v_tilde_next.copy()
        p_next = np.reshape(p_field_previous, shape = ((configs["N_CELLS_X"] + 1)*(configs["N_CELLS_Y"] + 1),))

        # Pre-compute constant values
        Au = np.diag(np.diag(Mu))
        Au_inv = np.diag(1/np.diag(Mu))
        Av = np.diag(np.diag(Mv))
        Av_inv = np.diag(1/np.diag(Mv))
        L = LaplacianMatrix(p_field_previous, dx, dy)
        L_with_bondaries = ApplyPressureBC(L, p_field_previous)

        # Linear iterations
        while iter_step < configs["N_ITER_STEP"] and not conv_criteria:
            iter_step+=1
            # Saves previous state to evaluate convergence
            u_old = u_next.copy()
            v_old = v_next.copy()
            p_old = p_next.copy()

            # Calculate soure term gradient in x direction
            u_prev_flat = np.reshape(u_field_previous, ((configs["N_CELLS_X"]+1)*(configs["N_CELLS_Y"]+1),))
            Hu = u_prev_flat/dt - (Mu - Au) @ u_next
            AHu_field = np.reshape(Au_inv @ Hu, shape = ((configs["N_CELLS_X"] + 1),(configs["N_CELLS_Y"] + 1)))
            dAHudx_field, _ = np.gradient((AHu_field), x, y)
            dAHudx_field[0,:] = dAHudx_field[-1,:] = 0.0
            dAHudx_field[:,0] = dAHudx_field[:,-1] = 0.0
            dAHudx = np.reshape(dAHudx_field, shape=((configs["N_CELLS_X"] + 1)*(configs["N_CELLS_Y"] + 1),))

            # Calculate soure term gradient in y direction
            v_prev_flat = np.reshape(v_field_previous, ((configs["N_CELLS_X"]+1)*(configs["N_CELLS_Y"]+1),))
            Hv = v_prev_flat/dt - (Mv - Av) @ v_next
            AHv_field = np.reshape(Av_inv @ Hv, shape = ((configs["N_CELLS_X"] + 1),(configs["N_CELLS_Y"] + 1)))
            _, dAHvdy_field = np.gradient(AHv_field, x, y)
            dAHvdy_field[0,:] = dAHvdy_field[-1,:] = 0.0
            dAHvdy_field[:,0] = dAHvdy_field[:,-1] = 0.0
            dAHvdy = np.reshape(dAHvdy_field, shape=((configs["N_CELLS_X"] + 1)*(configs["N_CELLS_Y"] + 1),))
            
            # Solves Laplace equation for Pressure
            p_next = np.linalg.solve(L_with_bondaries, Au @ dAHudx + Av @ dAHvdy)
            # Under-relaxation on P
            p_field_next = np.reshape(p_old + configs["ALPHA_P"] *(p_next - p_old), shape=((configs["N_CELLS_X"]+1),(configs["N_CELLS_Y"]+1)))
            dpdx_field_next, dpdy_field_next = np.gradient(p_field_next, x, y)

            # Find the corrected velocity U
            u_next = Au_inv @ Hu - Au_inv @ np.reshape(dpdx_field_next, shape = ((configs["N_CELLS_X"] + 1)*(configs["N_CELLS_Y"] + 1),))
            # Under-relaxation on U
            u_field_next = np.reshape(u_old + configs["ALPHA_U"] * (u_next - u_old), shape=((configs["N_CELLS_X"]+1),(configs["N_CELLS_Y"]+1)))
            ## No slip condition at wall u = 0 + open lid
            u_field_next[ 0,:] = 0
            u_field_next[-1,:] = 0
            u_field_next[:, 0] = 0
            u_field_next[:,-1] = configs["HORIZONTAL_VELOCITY_TOP"]
            
            # Find the corrected velocity U
            v_next = Av_inv @ Hv - Av_inv @ np.reshape(dpdy_field_next, shape = ((configs["N_CELLS_X"] + 1)*(configs["N_CELLS_Y"] + 1),))
            # Under-relaxation on U and V
            v_field_next = np.reshape(v_old + configs["ALPHA_V"] * (v_next - v_old), shape=((configs["N_CELLS_X"]+1),(configs["N_CELLS_Y"]+1)))
            ## No slip condition at wall v = 0
            v_field_next[ 0,:] = 0
            v_field_next[-1,:] = 0
            v_field_next[:, 0] = 0
            v_field_next[:,-1] = 0

            u_next = np.reshape(u_field_next, shape = ((configs["N_CELLS_X"] + 1)*(configs["N_CELLS_Y"] + 1),)).copy()
            v_next = np.reshape(v_field_next, shape = ((configs["N_CELLS_X"] + 1)*(configs["N_CELLS_Y"] + 1),)).copy()
            p_next = np.reshape(p_field_next, shape = ((configs["N_CELLS_X"] + 1)*(configs["N_CELLS_Y"] + 1),)).copy()

            # Calculate residuals
            u_residual = np.abs((u_next - u_old)).sum()
            v_residual = np.abs((v_next - v_old)).sum()
            p_residual = np.abs((p_next - p_old)).sum()

            if u_residual<configs["TOLERANCE_ITER"] and v_residual<configs["TOLERANCE_ITER"] and p_residual<configs["TOLERANCE_ITER"]:
                print(f"t = {t}, Linear Iterations:{iter_step}, Residuals:\n u_residual {u_residual}\n v_residual {v_residual}\n p_residual {p_residual}")    
                print("Converged")
                conv_criteria = True
            elif iter_step >= configs["N_ITER_STEP"]:
                print(f"t = {t}, Linear Iterations:{iter_step}, Residuals:\n u_residual {u_residual}\n v_residual {v_residual}\n p_residual {p_residual}")    
                print("Max. iter reached")
            else:
                print(f"  iter {iter_step}: u={u_residual:.3e} v={v_residual:.3e} p={p_residual:.3e}")

        u_field_previous = u_field_next.copy()
        v_field_previous = v_field_next.copy()
        p_field_previous = p_field_next.copy()

        # Update the values
        t+=dt

    results= {
        "domain" : {"X":X, "Y":Y},
        "results": {
                    "pressure": p_field_next,
                    "velocity":[
                        u_field_next, 
                        v_field_next
                        ]
                    }
            }

    return results

configs = {
            "N_CELLS_X" : 30,
            "N_CELLS_Y" : 20,
            "RUN_TIME" : 0.05,
            "KINEMATIC_VISCOSITY" : 0.1,
            "N_ITER_STEP" : 150,
            "TOLERANCE_ITER" : 10**(-3),
            "DENSITY" : 1.0,
            "HORIZONTAL_VELOCITY_TOP" : 1.0,
            "CFL" : 2,
            "ALPHA_P" : 0.8,
            "ALPHA_U" : 0.8,
            "ALPHA_V" : 0.8,
        }

# Main UI
@ui.page('/')
def main():

    async def get_data() -> None:
        global configs
        content = await editor.run_editor_method('get')
        configs = content['json']
        ui.notify(f'Updated!')

    async def handle_simulation():
        ui.notify(f'Simulation running...')
        result = await run.cpu_bound(Simulation, configs)
        plot_update(result)
        ui.notify(f'Simulation done!')

    def plot_update(results):
        X, Y = results["domain"]["X"], results["domain"]["Y"]
        u, v = results["results"]["velocity"]
        pressure = results["results"]["pressure"]
        with plot.figure as fig:
            ax = fig.gca()
            ax.clear()
            norm = cm.colors.Normalize(vmax=abs(pressure).max(), vmin=-abs(pressure).max())
            ax.contour(X, Y, pressure, norm=norm)
            ax.quiver(X, Y, u, v)

    with ui.row():
        with ui.column():
            with ui.row():
                editor = ui.json_editor({'content': {'json': configs}})


            ui.button('Update', on_click = get_data)
            ui.button('Run', on_click = handle_simulation)

        with ui.column():
            with ui.row():
                with ui.card():
                    plot = ui.matplotlib(figsize=(10, 5))

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
    # Simulation(configs)