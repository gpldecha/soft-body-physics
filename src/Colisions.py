def update_particle(position, previous, material, boundary_x, boundary_y):
    # screen boundaries
    x_min, x_max = boundary_x
    y_min, y_max = boundary_y

    if position[0] < x_min:
        distance = position - previous
        position[0] = x_min + (x_min - position[0])
        previous[0] = position[0] + material.bounce * distance[0]
        #
        update_distance_x(position, distance, material)
        return True

    elif position[0] > x_max:
        distance = position - previous
        position[0] = x_max - (position[0] - x_max)
        previous[0] = position[0] + material.bounce * distance[0]
        #
        update_distance_x(position, distance, material)
        return True

    if position[1] < y_min:
        distance = position - previous
        position[1] = y_min + (y_min - position[1])
        previous[1] = position[1] + material.bounce * distance[1]
        #
        update_distance_y(position, distance, material)
        return True

    elif position[1] > y_max:
        distance = position - previous
        position[1] = y_max - (position[1] - y_max)
        previous[1] = position[1] + material.bounce * distance[1]
        #
        update_distance_y(position, distance, material)
        return True

    return False


def update_particle_manipulator(position, previous, material, boundary_x, boundary_y):
    # manipulator boundaries
    x_min, x_max = boundary_x # (-0.1, 0.1)
    y_min, y_max = boundary_y

    if position[0] < x_max:
        distance = position - previous
        position[0] = x_max + (x_max - position[0])
        previous[0] = position[0] + material.bounce * distance[0]
        #
        update_distance_x(position, distance, material)


def update_distance_x(position, distance, material):
    j = distance[1]
    k = distance[0] * material.friction
    t = j
    if j != 0.0:
        t /= abs(j)
    if abs(j) <= abs(k):
        if j * t > 0.0:
            position[1] -= 2.0 * j
    else:
        if k * t > 0.0:
            position[1] -= k


def update_distance_y(position, distance, material):
    j = distance[0]
    k = distance[1] * material.friction
    t = j
    if j != 0.0:
        t /= abs(j)
    if abs(j) <= abs(k):
        if j * t > 0.0:
            position[0] -= 2.0 * j
    else:
        if k * t > 0.0:
            position[0] -= k