export interface MovementPattern {
    attack_north: boolean;
    attack_east: boolean;
    attack_south: boolean;
    attack_west: boolean;
    attack_southEast: boolean;
    attack_southWest: boolean;
    attack_northEast: boolean;
    attack_northWest: boolean;
    translate_north: boolean;
    translate_east: boolean;
    translate_south: boolean;
    translate_west: boolean;
    translate_southEast: boolean;
    translate_southWest: boolean;
    translate_northEast: boolean;
    translate_northWest: boolean;
    attack_jumps: [number, number][];
    translate_jumps: [number, number][];
    attack_slides: [number, number][][];
    translate_slides: [number, number][][];
  }

let patternA: MovementPattern = {
attack_north: false,
attack_east: false,
attack_south: false,
attack_west: false,
attack_southEast: false,
attack_southWest: false,
attack_northEast: false,
attack_northWest: false,
translate_north: false,
translate_east: false,
translate_south: false,
translate_west: false,
translate_southEast: false,
translate_southWest: false,
translate_northEast: false,
translate_northWest: false,
attack_jumps: [[-4, 0], [-4, 2], [-4, -2], [-2, 0], [-2, 2], [-2, -2], [-2, 4], [-2, -4], [-3, 1], [-3, 3], [-3, -1], [-3, -3], [-1, 1], [-1, 3], [-1, -1], [-1, -3], [0, 4], [0, -4], [0, 2], [0, -2], [1, 1], [1, 3], [1, -1], [1, -3], [3, 1], [3, 3], [3, -1], [3, -3], [4, 0], [4, 2], [4, -2], [2, 0], [2, 2], [2, -2], [2, -4], [2, 4]],
translate_jumps: [[-4, 0], [-4, 2], [-4, -2], [-2, 0], [-2, 2], [-2, -2], [-2, 4], [-2, -4], [-3, 1], [-3, 3], [-3, -1], [-3, -3], [-1, 1], [-1, 3], [-1, -1], [-1, -3], [0, 4], [0, -4], [0, 2], [0, -2], [1, 1], [1, 3], [1, -1], [1, -3], [3, 1], [3, 3], [3, -1], [3, -3], [4, 0], [4, 2], [4, -2], [2, 0], [2, 2], [2, -2],[2, -4], [2, 4]],
attack_slides: [],
translate_slides: [],
};

let patternB: MovementPattern = {
attack_north: false,
attack_east: false,
attack_south: false,
attack_west: false,
attack_southEast: false,
attack_southWest: false,
attack_northEast: false,
attack_northWest: false,
translate_north: false,
translate_east: false,
translate_south: false,
translate_west: false,
translate_southEast: false,
translate_southWest: false,
translate_northEast: false,
translate_northWest: false,
attack_jumps: [[-2, 2], [-2, 1], [-2, 0],[-2,-1], [-2, -2], [-1, 2], [-1, 1], [-1, 0], [-1, -1], [-1, -2], [0, 2], [0, 1], [0, -1], [0, -2], [1, 2], [1, 1], [1, 0], [1, -1], [1, -2], [2, 2], [2, 1], [2, 0], [2, -1], [2, -2]],
translate_jumps: [[-2, 2], [-2, 1], [-2, 0],[-2,-1], [-2, -2], [-1, 2], [-1, 1], [-1, 0], [-1, -1], [-1, -2], [0, 2], [0, 1], [0, -1], [0, -2], [1, 2], [1, 1], [1, 0], [1, -1], [1, -2], [2, 2], [2, 1], [2, 0], [2, -1], [2, -2]],
attack_slides: [],
translate_slides: [],
};

let patternC: MovementPattern = {
attack_north: true,
attack_east: true,
attack_south: true,
attack_west: true,
attack_southEast: true,
attack_southWest: true,
attack_northEast: true,
attack_northWest: true,
translate_north: true,
translate_east: true,
translate_south: true,
translate_west: true,
translate_southEast: true,
translate_southWest: true,
translate_northEast: true,
translate_northWest: true,
attack_jumps: [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1]],
translate_jumps: [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1]],
attack_slides: [],
translate_slides: [],
};

let patternD: MovementPattern = {
attack_north: true,
attack_east: true,
attack_south: true,
attack_west: true,
attack_southEast: true,
attack_southWest: true,
attack_northEast: true,
attack_northWest: true,
translate_north: true,
translate_east: true,
translate_south: false,
translate_west: true,
translate_southEast: false,
translate_southWest: false,
translate_northEast: true,
translate_northWest: true,
attack_jumps: [],
translate_jumps: [],
attack_slides: [],
translate_slides: [],
};

let patternE: MovementPattern = {
attack_north: true,
attack_east: true,
attack_south: true,
attack_west: true,
attack_southEast: false,
attack_southWest: false,
attack_northEast: false,
attack_northWest: false,
translate_north: true,
translate_east: true,
translate_south: true,
translate_west: true,
translate_southEast: false,
translate_southWest: false,
translate_northEast: false,
translate_northWest: false,
attack_jumps: [[3, 4], [3, -4], [4, 3], [4, -3], [-3, 4], [-3, -4], [-4, 3], [-4, -3], [5, 12], [5, -12], [12, 5], [12, -5], [-5, 12], [-5, -12], [-12, 5], [-12, -5]],
translate_jumps: [[3, 4], [3, -4], [4, 3], [4, -3], [-3, 4], [-3, -4], [-4, 3], [-4, -3], [5, 12], [5, -12], [12, 5], [12, -5], [-5, 12], [-5, -12], [-12, 5], [-12, -5]],
attack_slides: [],
translate_slides: [],
};

let patternF: MovementPattern = {
attack_north: true,
attack_east: true,
attack_south: true,
attack_west: true,
attack_southEast: false,
attack_southWest: false,
attack_northEast: false,
attack_northWest: false,
translate_north: true,
translate_east: true,
translate_south: true,
translate_west: true,
translate_southEast: false,
translate_southWest: false,
translate_northEast: false,
translate_northWest: false,
attack_jumps: [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1]],
translate_jumps: [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1]],
attack_slides: [],
translate_slides: [],
};

  export const DefaultCustomPatterns: MovementPattern[] = [
    patternA,
    patternB,
    patternC,
    patternD,
    patternE,
    patternF,
  ];