import QtQuick 2.12
import QtQuick.Window 2.12
import QtCharts 2.14
import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3

ApplicationWindow {
    id: root
    width: 1050
    height: 630
    visible: true
    title: "Fourier Series Demo"
    Rectangle {
        id: recroot
        width: root.width
        height: root.height

        color: "white" //"#e1e6db" //"#adafab"
        clip: false

        Grid {
            id: gridCustom
            x: 602
            y: 65//58
            width: 272
            height: 452
            clip: false
            anchors.right: parent.right
            anchors.rightMargin: 20
            columns: 1
            spacing: 50

            Grid {
                columns: 1
                spacing: 10
                Rectangle {
                    id: recSigType
                    width: gridCustom.width
                    height: 25
                    color: "#60bce1"//"#79b554"
                    clip: false

                    Label {
                        id: lblSignalType
                        color: "#ffffff"
                        text: qsTr("Choose the signal type:")
                        anchors.fill: parent
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                    }
                }

                ComboBox {
                    id: cbxSignaltypes
                    height: 30
                    font.pointSize: 10
                    rightPadding: 0
                    focusPolicy: Qt.TabFocus
                    font.weight: Font.Normal
                    width: parent.width - 35
                    flat: false
                    editable: false
                    currentIndex: 0
                    model: ["Square",
                        "Triangle", "Ramp or Sawtooth",
                        "Full-Wave Rectified Sine",
                        "Full-Wave Rectified Cosine",
                        "Half-Wave Rectified Sine",
                        "Half-Wave Rectified Cosine"]

                    onFocusChanged: {


                    }

                    onCurrentValueChanged: {

                        // GET VALUES
                        FS.updateYval(cbxSignaltypes.currentIndex, sliderPeriod.value)
                        FS.updateSynthesized(sliderFC.value, cbxSignaltypes.currentIndex, sliderPeriod.value)

                        var timeaxis = FS.timeaxis
                        var yval = FS.yval
                        var synthesized = FS.synthesized
                        var absMag = FS.abs_mag
                        var angMag = FS.ang_mag
                        var n = 0

                        // Clear previous Signal's plot
                        originalSignal.clear()
                        synthrsizedSignal.clear()
                        errorSignal.clear()
                        magSpectrum.clear()
                        phaseSpectrum.clear()

                        // Check if error show CheckBox is true or not

                        if (chbxShowError.checked == true) {
                            originalSignal.visible = false
                            synthrsizedSignal.visible = false
                            errorSignal.visible = true

                            for(var i = 0; i < yval.length; i++){

                                errorSignal.append(timeaxis[i], yval[i]- synthesized[i])
                            }

                            for(var j = -sliderFC.value; j <= sliderFC.value; j++){

                                magSpectrum.append(j, absMag[n])
                                phaseSpectrum.append(j, angMag[n])
                                n = n+1
                            }


                        }else {

                            originalSignal.visible = true
                            synthrsizedSignal.visible = true
                            errorSignal.visible = false


                            for(var j = 0; j < yval.length; j++){

                                originalSignal.append(timeaxis[j], yval[j])
                                synthrsizedSignal.append(timeaxis[j], synthesized[j])

                            }

                            for(var j = -sliderFC.value; j <= sliderFC.value; j++){

                                magSpectrum.append(j, absMag[n])
                                phaseSpectrum.append(j, angMag[n])
                                n = n+1
                            }


                        }

                        // set axis
                        waveAxisX.min = timeaxis[0]; waveAxisX.max = timeaxis[timeaxis.length -1]
                        waveAxisY.min = -1.2; waveAxisY.max = 1.2


                    } // onCurrentValueChanged


                }
            }

            Grid{
                columns: 1
                spacing: 10
                Rectangle {
                    id: recSetPeriod
                    width: gridCustom.width
                    height: 25
                    color: "#60bce1"
                    Label {
                        id: lblSetPeriod
                        color: "#ffffff"
                        text: qsTr("Choose The Signal Period: T =  " + sliderPeriod.value)
                        verticalAlignment: Text.AlignVCenter
                        anchors.fill: parent
                        horizontalAlignment: Text.AlignHCenter
                    }
                    clip: false
                }

                Slider {
                    id: sliderPeriod
                    width: parent.width
                    height: 29
                    from: 5
                    value: 10
                    to: 25
                    onValueChanged: {

                        // change the label text
                        lblSetPeriod.text = "Choose The Signal Period: T = " + parseFloat(value).toFixed(3);


                        // GET VALUES
                        FS.updateYval(cbxSignaltypes.currentIndex, sliderPeriod.value)
                        FS.updateSynthesized(sliderFC.value, cbxSignaltypes.currentIndex, sliderPeriod.value)

                        var timeaxis = FS.timeaxis
                        var yval = FS.yval
                        var synthesized = FS.synthesized

                        // Clear previous Signal's plot
                        originalSignal.clear()
                        synthrsizedSignal.clear()
                        errorSignal.clear()

                        // Check if error show CheckBox is true or not

                        if (chbxShowError.checked == true) {
                            originalSignal.visible = false
                            synthrsizedSignal.visible = false
                            errorSignal.visible = true

                            for(var i = 0; i < yval.length; i++){

                                errorSignal.append(timeaxis[i], yval[i]- synthesized[i])
                            }

                        }else {

                            originalSignal.visible = true
                            synthrsizedSignal.visible = true
                            errorSignal.visible = false


                            for(var j = 0; j < yval.length; j++){

                                originalSignal.append(timeaxis[j], yval[j])
                                synthrsizedSignal.append(timeaxis[j], synthesized[j])

                            }


                        }

                        // set axis
                        waveAxisX.min = timeaxis[0]; waveAxisX.max = timeaxis[timeaxis.length -1]
                        waveAxisY.min = -1.2; waveAxisY.max = 1.2


                    }

                }

            }
            Grid {
                columns: 1
                spacing: 10
                Rectangle {
                    id: recInfFC // FC = fourier coefficients
                    width: gridCustom.width
                    height: 90
                    color: "#60bce1"
                    Text {
                        id: lblInfFC
                        color: "#ffffff"
                        text: qsTr("Choose the number of fourier \n coefficients by entering a number\n between 0 and 15 in the edit box or \n use the slider")
                        verticalAlignment: Text.AlignVCenter
                        anchors.fill: parent
                        horizontalAlignment: Text.AlignHCenter
                    }
                    clip: false
                }

                Rectangle {
                    id: recSetFC
                    width: gridCustom.width
                    height: 25
                    color: "#60bce1"
                    Label {
                        id: lblSetFC
                        color: "#ffffff"
                        text: qsTr("The Number of Cofficient is = 0 ")
                        verticalAlignment: Text.AlignVCenter
                        anchors.fill: parent
                        horizontalAlignment: Text.AlignHCenter
                    }

                    clip: false
                }


                Grid {
                    columns: 2
                    spacing: 10
                    verticalItemAlignment: Grid.AlignVCenter
                    Slider {
                        id: sliderFC
                        width: 230
                        height: 30
                        from: 0
                        value: 0
                        stepSize: 1
                        to: 15
                        onValueChanged: {

                            // change lblSetFC text
                            if(value == 0)
                                lblSetFC.text = "DC Coefficient: K = " + value
                            else
                                lblSetFC.text = "Coefficients from k = "+ -value + " to k = " + value

                            txtShowCoeff.text = sliderFC.value

                            // GET VALUES
                            FS.updateYval(cbxSignaltypes.currentIndex, sliderPeriod.value)
                            FS.updateSynthesized(sliderFC.value, cbxSignaltypes.currentIndex, sliderPeriod.value)

                            var timeaxis = FS.timeaxis
                            var yval = FS.yval
                            var synthesized = FS.synthesized
                            var absMag = FS.abs_mag
                            var angMag = FS.ang_mag
                            var n = 0


                            // Clear previous Signal's plot
                            originalSignal.clear()
                            synthrsizedSignal.clear()
                            errorSignal.clear()

                            // Check if error show CheckBox is true or not

                            if (chbxShowError.checked == true) {
                                originalSignal.visible = false
                                synthrsizedSignal.visible = false
                                errorSignal.visible = true

                                for(var i = 0; i < yval.length; i++){

                                    errorSignal.append(timeaxis[i], yval[i]- synthesized[i])
                                }

                            }else {

                                originalSignal.visible = true
                                synthrsizedSignal.visible = true
                                errorSignal.visible = false


                                for(var j = 0; j < yval.length; j++){

                                    originalSignal.append(timeaxis[j], yval[j])
                                    synthrsizedSignal.append(timeaxis[j], synthesized[j])

                                }


                            }

                            // set axis
                            waveAxisX.min = timeaxis[0]; waveAxisX.max = timeaxis[timeaxis.length -1]
                            waveAxisY.min = -1.2; waveAxisY.max = 1.2
                            //-------------Magnitude Spectrum ------------------//
                            magSpectrum.clear()
                            phaseSpectrum.clear()
                            for(var j = -sliderFC.value; j <= sliderFC.value; j++){

                                magSpectrum.append(j, absMag[n])
                                phaseSpectrum.append(j, angMag[n])
                                n = n+1
                            }

                        }



                    }

                    Rectangle {
                        id: recShowCoeff
                        width: 30
                        height: 30
                        color: "#ffffff"
                        Text {
                            id: txtShowCoeff
                            anchors.fill: parent
                            text: "0"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            font.weight: Font.Light
                            font.pixelSize: 17
                        }
                    }
                }

            }

        }

        Frame {
            id: waveform
            x: 37
            y: 58
            width: 665
            height: 185
            anchors.top: parent.top
            anchors.topMargin: 52
            bottomPadding: -15
            rightPadding: -9
            leftPadding: -9
            topPadding: -15

            ChartView {
                id: chartSignal
                anchors.fill: parent
                antialiasing: true
                animationOptions: ChartView.SeriesAnimations
                legend.visible: true
                legend.markerShape: Legend.MarkerShapeFromSeries
                legend.alignment: Qt.AlignTop
                margins.top: 0
                margins.bottom: 0
                margins.left: 0
                margins.right: 0

                ValueAxis {
                    id: waveAxisY
                }

                ValueAxis {
                    id: waveAxisX
                }

                LineSeries {
                    id: originalSignal
                    name: "Original Signal"
                    axisX: waveAxisX
                    axisY: waveAxisY
                    width: 0.5
                }

                LineSeries {
                    id: synthrsizedSignal
                    name: "Synthrsized Signal "
                    color: "red"
                    axisX: waveAxisX
                    axisY: waveAxisY

                    width: 1
                }
                LineSeries {
                    id: errorSignal
                    name: "Error Signal"
                    axisX: waveAxisX
                    axisY: waveAxisY
                    visible: false  // important point to delete duplicates
                    color: "blue"
                    width: 1
                }

                Component.onCompleted:
                {
//                    // Set default value of GUI components & Create default plots
//                    sliderPeriod.value = 10
//                    sliderFC.value = 0
//                    cbxSignaltypes.currentIndex = 0

//                    FS.updateYval(cbxSignaltypes.currentIndex, sliderPeriod.value)
//                    FS.updateSynthesized(sliderFC.value, cbxSignaltypes.currentIndex, sliderPeriod.value)

//                    var timeaxis = FS.timeaxis
//                    var yval = FS.yval
//                    var synthesized = FS.synthesized
//                    var absMag = FS.abs_mag
//                    var angMag = FS.ang_mag
//                    var n = 0


//                    for(var i = 0; i < yval.length; i++){

//                        originalSignal.append(timeaxis[i], yval[i])
//                        synthrsizedSignal.append(timeaxis[i], synthesized[i])
//                        errorSignal.append(timeaxis[i], yval[i]- synthesized[i])

//                    }


//                    // set axis
//                    waveAxisX.min = timeaxis[0]; waveAxisX.max = timeaxis[timeaxis.length -1]
//                    waveAxisY.min = -1.2; waveAxisY.max = 1.2


                }

            }

        }

        Frame {
            id: magnitude
            x: 37
            y: 223
            width: 665
            height: 150
            anchors.top: chbxShowError.bottom
            anchors.topMargin: 10

            bottomPadding: -11
            rightPadding: -9
            leftPadding: -9
            topPadding: -17


            ChartView {
                id: magnitutde
                anchors.fill: parent
                antialiasing: true
                animationOptions: ChartView.SeriesAnimations
                legend.visible: false
                // Delete margins
                margins.top: 0
                margins.bottom: 0
                margins.left: 0
                margins.right: 0



                ValueAxis {
                    id: magAxisX
                    min: -15
                    max: 15

                }

                ScatterSeries  {
                    id: magSpectrum
                    axisX: magAxisX

                    markerSize: 10

                }

            }
        }

        Frame {
            id: fphase
            x: 37
            y: 388
            width: 665
            height: 150
            contentWidth: 0
            anchors.top: chbxCoeffFreq.bottom
            anchors.topMargin: 10
            bottomPadding: -11
            rightPadding: -9
            leftPadding: -9
            topPadding: -19

            ChartView {
                id: phase
                anchors.fill: parent
                antialiasing: true
                animationOptions: ChartView.SeriesAnimations
                legend.visible: false

                margins.top: 0
                margins.bottom: 0
                margins.left: 0
                margins.right: 0

                ValueAxis {
                    id: phaseAxisY
                    min: -Math.PI - 0.5
                    max: Math.PI + 0.5
                }
                ValueAxis {
                    id: phaseAxisX
                    min: -15
                    max: 15
                    tickCount: 15
                }

                ScatterSeries  {
                    id: phaseSpectrum
                    axisY: phaseAxisY
                    axisX: phaseAxisX
                    markerSize: 10


                }

            }
        }

        CheckBox {

            id: chbxShowError
            x: 569
            y: 167
            width: 133
            height: 15
            text: qsTr("Show Error")
            font.bold: false
            anchors.top: waveform.bottom
            anchors.topMargin: 6
            checked: false

            // Resizing checkbox
            indicator.width: 15
            indicator.height: 15
            onCheckedChanged: {

                // GET VALUES
                FS.updateYval(cbxSignaltypes.currentIndex, sliderPeriod.value)
                FS.updateSynthesized(sliderFC.value, cbxSignaltypes.currentIndex, sliderPeriod.value)

                var timeaxis = FS.timeaxis
                var yval = FS.yval
                var synthesized = FS.synthesized

                // Clear previous Signal's plot
                originalSignal.clear()
                synthrsizedSignal.clear()
                errorSignal.clear()

                // Check if error show CheckBox is true or not

                if (chbxShowError.checked == true) {
                    originalSignal.visible = false
                    synthrsizedSignal.visible = false
                    errorSignal.visible = true

                    for(var i = 0; i < yval.length; i++){

                        errorSignal.append(timeaxis[i], yval[i]- synthesized[i])
                    }

                }else {

                    originalSignal.visible = true
                    synthrsizedSignal.visible = true
                    errorSignal.visible = false


                    for(var j = 0; j < yval.length; j++){

                        originalSignal.append(timeaxis[j], yval[j])
                        synthrsizedSignal.append(timeaxis[j], synthesized[j])

                    }


                }

                // set axis
                waveAxisX.min = timeaxis[0]; waveAxisX.max = timeaxis[timeaxis.length -1]
                waveAxisY.min = -1.2; waveAxisY.max = 1.2

            }
        }

        CheckBox {
            id: chbxCoeffFreq
            x: 578
            y: 339
            width: 124
            height: 21
            text: qsTr("coeff/ freq.")
            font.bold: false
            anchors.top: magnitude.bottom
            anchors.topMargin: 0

            // Resizing checkbox
            indicator.width: 15
            indicator.height: 15
            onCheckedChanged: {



            }

        }

        Rectangle {
            id: rectangle
            x: 15
            y: 150
            width: 90
            height: 22
            color: "#ffffff"

            Text {
                id: lblAmp
                text: qsTr("Amplitude")
                font.bold: true
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
                font.pixelSize: 15
            }
            transform: Rotation {
                origin.x: 25
                origin.y: 25
                angle: -90
            }
        }

        Rectangle {
            id: recSecond
            x: 307
            y: 266
            width: 126
            height: 23
            anchors.top: waveform.bottom
            color: "#ffffff"

            Text {
                id: lblsecond
                text: qsTr("Time (seconds)")
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                font.bold: true
                anchors.fill: parent
                font.pixelSize: 15
            }
        }



        Rectangle {
            id: recMagAmp
            x: 15//37
            y: 320//340//98
            width: 90
            height: 22
            color: "#ffffff"

            Text {
                id: lblMagAmp
                text: qsTr("Amplitude")
                font.bold: true
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
                font.pixelSize: 15
            }
            transform: Rotation {
                origin.x: 25
                origin.y: 25
                angle: -90
            }
        }

        Rectangle {
            id: recPhase
            x: 15//37
            y: 510//550//98
            width: 90
            height: 22
            color: "#ffffff"


            Text {
                id: lblPhase
                text: qsTr("Phase")
                font.bold: true
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
                font.pixelSize: 15
            }
            transform: Rotation {
                origin.x: 25
                origin.y: 25
                angle: -90
            }
        }


        Rectangle {
            id: recFC
            x: 307
            y: 266
            width: 126
            height: 23
            anchors.top: magnitude.bottom
            color: "#ffffff"

            Text {
                id: lblFC
                text: qsTr("Number of Fourier Coefficients")
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                font.bold: true
                anchors.fill: parent
                font.pixelSize: 15
            }
        }


        Rectangle {
            id: recFC2
            x: 307
            y: 266
            width: 126
            height: 23
            anchors.top: fphase.bottom
            color: "#ffffff"

            Text {
                id: lblFC2
                text: qsTr("Number of Fourier Coefficients")
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                font.bold: true
                anchors.fill: parent
                font.pixelSize: 15
            }
        }


        Rectangle {
            id: recLblWave
            x: 52
            y: 21
            width: 100
            height: 25

            color: "#d3f3a3"
            anchors.bottom: waveform.top
            anchors.bottomMargin: -49
            anchors.left: waveform.left
            anchors.leftMargin: 43

            Label {
                id: lblWave
                text: qsTr("WaveForm of the")
                //                font.bold: true
                font.pointSize: 10
                //                font.italic: true
                font.weight: Font.Light
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
            }
        }


        Rectangle {
            id: recLblMagSpec
            x: 52
            y: 21
            width: 115
            height: 25

            color: "#d3f3a3"
            anchors.bottom: magnitude.top
            anchors.bottomMargin: -2
            anchors.left: magnitude.left
            anchors.leftMargin: 41

            Label {
                id: lblMagSpec
                text: qsTr("Magnitude Spectrum")
                //                font.bold: true
                font.pointSize: 10
                //                font.italic: true
                font.weight: Font.Light
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
            }
        }

        Rectangle {
            id: recLblPhaseSpec
            x: 52
            y: 21
            width: 100
            height: 25

            color: "#d3f3a3"
            anchors.bottom: fphase.top
            anchors.bottomMargin: -2
            anchors.left: fphase.left
            anchors.leftMargin: 41

            Label {
                id: lblPhasespec
                text: qsTr("Phase Spectrum")
                //                font.bold: true
                font.pointSize: 10
                //                font.italic: true
                font.weight: Font.Light
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
            }
        }





    }

}


