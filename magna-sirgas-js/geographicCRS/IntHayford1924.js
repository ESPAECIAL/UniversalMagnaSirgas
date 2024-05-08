const EllipsoidalCRS = require('./EllipsoidalCRS');
const proj4List = require('proj4-list');

class IntHayford1924 extends EllipsoidalCRS {
    constructor() {
        super();
    }

    nameFromPrj() {
        return "intl";
    }

    crs() {
        return proj4List["EPSG:4022"];
    }

    toString() {
        return `IntHayford1924 is ${IntHayford1924.crsType()} coming from PROJ (${IntHayford1924.crs()}) with limits in longitude (${this.maxEast()}, ${this.minWest()}) and in latitude (${this.maxNorth()}, ${this.minSouth()})`;
    }
}

module.exports = IntHayford1924;