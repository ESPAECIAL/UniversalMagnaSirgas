const Ellipsoidal = require('./EllipsoidalCRS');
const proj4List = require('proj4-list');

class WGS1984 extends Ellipsoidal {
    constructor() {
        super();
    }

    nameFromPrj() {
        return "wgs84";
    }

    crs() {
        return proj4List["EPSG:4326"];
    }

    toString() {
        return `WGS1984 is ${WGS1984.crsType()} coming from PROJ (${WGS1984.crs()}) with limits in longitude (${this.max_east()}, ${this.min_west()}) and in latitude (${this.max_north()}, ${this.min_south()})`;
    }

}

module.exports = WGS1984;