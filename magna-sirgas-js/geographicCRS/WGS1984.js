const Ellipsoidal = require('./EllipsoidalCRS');
const proj4 = require('proj4');

class WGS1984 extends Ellipsoidal {
    constructor() {
        super();
        this._crs = proj4.defs('wgs84_crs', '+proj=longlat +ellps=WGS84');
        this._proj_name = "wgs84";
    }

    name_from_prj() {
        return this._proj_name;
    }

    crs() {
        return this._crs;
    }

    max_north() {
        return this._max_north;
    }

    min_south() {
        return this._min_south;
    }

    max_east() {
        return this._max_east;
    }

    min_west() {
        return this._min_west;
    }

    hashCode() {
        const crsString = JSON.stringify(this._crs);
        return crypto.createHash('md5').update(crsString).digest('hex');
    }

    equals(value) {
        return this._crs === value._crs;
    }

    toString() {
        return `WGS1984 is ${WGS1984._crs_type} coming from PROJ (${WGS1984._crs}) with limits in longitude (${this.max_east()}, ${this.min_west()}) and in latitude (${this.max_north()}, ${this.min_south()})`;
    }
}

module.exports = WGS1984;