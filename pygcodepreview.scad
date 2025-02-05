//!OpenSCAD

//gcodepreview 0.7, see gcodepreview.scad

 module osetupstock(stockXwidth, stockYheight, stockZthickness, zeroheight, stockzero) {
     psetupstock(stockXwidth, stockYheight, stockZthickness, zeroheight, stockzero);
 }

//function getxpos() = xpos();
//function getypos() = ypos();
//function getzpos() = zpos();
//function gettzpos() = tzpos();
//
//module setxpos(newxpos) {
//    psetxpos(newxpos);
//}
//
//module setypos(newypos) {
//    psetypos(newypos);
//}
//
//module setzpos(newzpos) {
//    psetzpos(newzpos);
//}
//
//module settzpos(newtzpos) {
//    psettzpos(newtzpos);
//}
//
module osettool(tn){
    psettool(tn);
}

function current_tool() = pcurrent_tool();

function otool_diameter(td_tool, td_depth) = ptool_diameter(td_tool, td_depth);

module oopengcodefile(fn) {
    popengcodefile(fn);
}

module oopendxffile(fn) {
//    echo(fn);
    popendxffile(fn);
}

module oopendxflgblfile(fn) {
    popendxflgblfile(fn);
}

module oopendxflgsqfile(fn) {
    popendxflgsqfile(fn);
}

module oopendxflgVfile(fn) {
    popendxflgVfile(fn);
}

module oopendxfsmblfile(fn) {
    popendxfsmblfile(fn);
}

module oopendxfsmsqfile(fn) {
//    echo(fn);
    popendxfsmsqfile(fn);
}

module oopendxfsmVfile(fn) {
    popendxfsmVfile(fn);
}

module oopendxfKHfile(fn) {
    popendxfKHfile(fn);
}

module oopendxfDTfile(fn) {
    popendxfDTfile(fn);
}

module owritecomment(comment) {
    writeln("(",comment,")");
}

module dxfwriteone(first) {
    writedxf(first);
//    writeln(first);
//    echo(first);
}

module dxfwritelgbl(first) {
    writedxflgbl(first);
}

module dxfwritelgsq(first) {
    writedxflgsq(first);
}

module dxfwritelgV(first) {
    writedxflgV(first);
}

module dxfwritesmbl(first) {
    writedxfsmbl(first);
}

module dxfwritesmsq(first) {
    writedxfsmsq(first);
}

module dxfwritesmV(first) {
    writedxfsmV(first);
}

module dxfwriteKH(first) {
    writedxfKH(first);
}

module dxfwriteDT(first) {
    writedxfDT(first);
}

module owriteone(first) {
    writeln(first);
}

module owritetwo(first, second) {
    writeln(first, second);
}

module owritethree(first, second, third) {
    writeln(first, second, third);
}

module owritefour(first, second, third, fourth) {
    writeln(first, second, third, fourth);
}

module owritefive(first, second, third, fourth, fifth) {
    writeln(first, second, third, fourth, fifth);
}

module owritesix(first, second, third, fourth, fifth, sixth) {
    writeln(first, second, third, fourth, fifth, sixth);
}

module owriteseven(first, second, third, fourth, fifth, sixth, seventh) {
    writeln(first, second, third, fourth, fifth, sixth, seventh);
}

module owriteeight(first, second, third, fourth, fifth, sixth, seventh,eighth) {
    writeln(first, second, third, fourth, fifth, sixth, seventh,eighth);
}

module owritenine(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth) {
    writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth);
}

module owriteten(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth) {
    writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth);
}

module owriteeleven(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh) {
    writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh);
}

module owritetwelve(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth) {
    writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth);
}

module owritethirteen(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth) {
    writeln(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth);
}

module oclosegcodefile() {
    pclosegcodefile();
}

module oclosedxffile() {
    pclosedxffile();
}

module oclosedxflgblfile() {
    pclosedxflgblfile();
}

module oclosedxflgsqfile() {
    pclosedxflgsqfile();
}

module oclosedxflgVfile() {
    pclosedxflgVfile();
}

module oclosedxfsmblfile() {
    pclosedxfsmblfile();
}

module oclosedxfsmsqfile() {
    pclosedxfsmsqfile();
}

module oclosedxfsmVfile() {
    pclosedxfsmVfile();
}

module oclosedxfDTfile() {
    pclosedxfDTfile();
}

module oclosedxfKHfile() {
    pclosedxfKHfile();
}

