import torch

collision = torch.zeros([500, ], dtype=torch.bool)


def getCollisions():
    return collision


def get_parameters(args):
    if args.tune_mppi <= 0:
        args.α = 0  # 5.94e-1
        args.λ = 40  # 1.62e1
        args.σ = 0.2  # 4.0505  # 10.52e1
        args.χ = 2.00e-2
        args.ω1 = 15.37
        args.ω2 = 9.16e3
        args.ω_Φ = 5.41

    K = 500
    T = 15
    Δt = 0.01

    dtype = torch.double
    device = 'cpu'

    α = args.α
    λ = args.λ
    Σ = args.σ * torch.tensor([
        [1, args.χ, args.χ],
        [args.χ, 1, args.χ],
        [args.χ, args.χ, 1]
    ], dtype=dtype, device=device)

    def dynamics(x, u):
        u[:, 2] = 0
        new_vel = x[:, 3:6] + u  # * Δt  # + pt1_vel
        new_vel = torch.clamp(new_vel, min=-1.7, max=1.7)
        # evtl noch die halbe zusätzliche neue Velocity dazuaddieren
        new_pos = x[:, 0:3] + new_vel * Δt  # + 0.5 * u * Δt * Δt  # new_vel * Δt  # + (pt1_vel / 2) * Δt

        return torch.cat((new_pos, new_vel), dim=1)

    def state_cost(x, goal, obstacles):
        global collision
        cost = 1000 * torch.norm((x[:, 0:3] - goal), dim=1) ** 2
        # cost -= args.ω1 * torch.norm(x[:, 3:6], dim=1) ** 2  # TODO Do we need this cost term?
        hand_dimension = torch.tensor([0.025, 0.1, 0.05])  # X-Lenght: 0.05, Y-Lenght: 0.2, Z-Lenght: 0.653
        finger_dimension = torch.tensor([0.00875, 0.013, 0.025])  # X-Lenght: 0.0175, Y-Lenght: 0.026, Z-Lenght: 0.05
        hand = x[:, :3].clone()
        hand[:, 2] += 0.16  # Distance from eef to Collision Center of Hand  # hand_dimension[2] + finger_dimension[2]

        table_collision = torch.le(x[:, 2], 0.3)

        dist1 = torch.abs(x[:, 0:3] - torch.tensor(obstacles[0:3], device=device))
        dist2 = torch.abs(x[:, 0:3] - torch.tensor(obstacles[6:9], device=device))
        collision = torch.logical_or(collision,
                                     torch.all(torch.le(dist1,
                                                        torch.tensor(obstacles[3:6], device=device) + torch.tensor(
                                                            [0.055, 0.055, 0.03])),
                                               dim=1))
        collision = torch.logical_or(collision,
                                     torch.all(
                                         torch.le(dist2,
                                                  torch.tensor(obstacles[9:12],
                                                               device=device) + torch.tensor(
                                                      [0.055, 0.055, 0.03])),
                                         dim=1))

        # Collision Detection with Hand
        dist3 = torch.abs(hand[:, 0:3] - torch.tensor(obstacles[0:3], device=device))
        dist4 = torch.abs(hand[:, 0:3] - torch.tensor(obstacles[6:9], device=device))
        collision = torch.logical_or(collision,
                                     torch.all(torch.le(dist3,
                                                        torch.tensor(obstacles[3:6], device=device) + hand_dimension),
                                               dim=1))
        collision = torch.logical_or(collision,
                                     torch.all(torch.le(dist4,
                                                        torch.tensor(obstacles[9:12], device=device) + hand_dimension),
                                               dim=1))
        # collision = torch.logical_or(collision,
        #                             border_collision)

        # collision = torch.logical_or(collision,
        #                             collision_reachable_workspace)

        if torch.any(collision):
            # print("Trajectorie with collision detected!")
            pass

        if torch.all(collision):
            print("All Trajectorie with collision detected!")
            pass

        # cost += 100 * border_collision
        cost += 100 * table_collision
        cost += args.ω2 * collision

        return cost

    def terminal_cost(x, goal):
        global collision
        cost = 10 * torch.norm((x[:, 0:3] - goal), dim=1) ** 2
        cost += args.ω_Φ * torch.norm(x[:, 3:6], dim=1) ** 2
        collision = torch.zeros([500, ], dtype=torch.bool)
        return cost

    def convert_to_target(x, u):
        new_vel = x[3:6] + u / (1 - torch.exp(torch.tensor(-0.01 / 0.100)))
        target_pos = x[0:3] + new_vel * Δt
        return x[0:3] + new_vel * Δt  # + u * Δt  # x[3:6] * Δt

    return K, T, Δt, α, dynamics, state_cost, terminal_cost, Σ, λ, convert_to_target, dtype, device
