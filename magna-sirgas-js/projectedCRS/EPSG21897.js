const ProjectedCRS = require('./ProjectedCRS');
const proj4List = require('proj4-list');

class EPSG21897 extends ProjectedCRS{

    constructor() {
        super();
    }

    crs() {
        return proj4List["EPSG:21897"];
    }

    maxNorth() {
        return 1799074.0;
    }

    minSouth() {
        return 213804.0;
    }

    maxEast() {
        return 1163585.2414666042;
    }

    minWest() {
        return 832143.631295867;
    }

    projName() {
        return 'Bogota 1975 / Colombia Bogota zone';
    }

    equals(value) {
        return this.crs() === value;
    }

    toString() {
        return `EPSG21897 is ${EPSG21897.crsType()} coming from PROJ (${this.crs()}) with limits in east (${this.maxEast()}, ${this.minWest()} and in north (${this.maxNorth()}, ${this.minSouth()}))`;
    }

}

module.exports = EPSG21897;