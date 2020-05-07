import QtQuick 2.12
import QtQuick.Window 2.12
import QtCharts 2.0
import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3


ApplicationWindow {

    id: root
    width: 700
    height: 630
    visible: true
    title: "sindrill"


    Rectangle {

        id: recRoot
        anchors.fill: parent

        MenuBar {
            x:0; y:0
            width: parent.width

            Menu {
                id: menuAnswers
                title: qsTr("&Answers")
                Action { id: aAnsw;text: qsTr("A = ") }
                Action { id: f0Answ;text: qsTr("f_0 = ") }
                Action { id: phiAnsw;text: qsTr("phi = ") }
            }

            Menu {
                title: qsTr("&Options")
                Menu {
                    title: qsTr("&Levels")
                    MenuItem {id:actNovice;checkable: true; checked: true; text: qsTr("&Novice"); onCheckedChanged: {
                            if (checked == true){
                                actPro.checked = false
                            }
                        }
                    }

                    MenuItem {id:actPro;checkable: true; text: qsTr("&Pro"); onCheckedChanged: {
                            if(checked == true) {
                                actNovice.checked = false
                            }

                        }
                    }
                }

                Action { text: qsTr("&Take Screen shot") }
                Action { text: qsTr("&Show Menu") }
            }

            Menu {
                title: qsTr("&Help")
                Action { text: qsTr("&Contents");
                    onTriggered: {
                        Qt.openUrlExternally("https://github.com/atzengin/spfirst");
                    }
                }
            }
        }

        Frame {
            id: ioFrame
            x: parent.width/2 - ioFrame.width/2
            y: 40
            width: root.width
            height: 223
            font.preferShaping: true
            wheelEnabled: false
            hoverEnabled: true
            enabled: true
            smooth: false
            antialiasing: false
            font.family: "Tahoma"
            contentHeight: 1
            font.wordSpacing: 0.1
            bottomPadding: 0
            rightPadding: 0
            leftPadding: 0
            topPadding: 0
            font.pointSize: 9

            Rectangle {
                id: recQuiz
                color: "#c9c1bf"
                border.color: "#00000000"
                anchors.fill: parent
                anchors.centerIn: parent



                Row {
                    id: rowInput
                    x: ioFrame.width/2 - rowInput.width/2 - 30
                    y: 80
                    width: 600
                    height: 32
                    spacing: 3
                    leftPadding: 0
                    rightPadding: 0

                    Row {
                        id: rowAmplitude
                        width: 223
                        height: 31
                        spacing: 1

                        Text {
                            id: element
                            text: qsTr("A = ")
                            font.weight: Font.Medium
                            font.bold: true
                            lineHeight: 1
                            fontSizeMode: Text.FixedSize
                            font.pixelSize: 17
                        }

                        Rectangle {
                            id: recAmp
                            width: 80
                            height: 28
                            color: "#ffffff"

                            TextInput {
                                id: amplitudeInput
                                anchors.fill: parent
                                font.family: "Verdana"
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                                font.weight: Font.Light
                                font.pixelSize: 17
                                text: '0'
                            }
                        }
                    }

                    Row {
                        id: rowF0
                        width: 223
                        height: 31
                        spacing: 1
                        Text {
                            id: txtF0
                            text: qsTr("f_0 = ")
                            fontSizeMode: Text.FixedSize
                            font.weight: Font.Medium
                            font.bold: true
                            font.pixelSize: 17
                            lineHeight: 1
                        }

                        Rectangle {
                            id: recF0
                            width: 80
                            height: 28
                            color: "#ffffff"
                            TextInput {
                                id: f0Input
                                anchors.fill: parent
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                                font.weight: Font.Light
                                font.pixelSize: 17
                                font.family: "Verdana"
                                text: '0'
                            }
                        }
                    }

                    Row {
                        id: rowPhi
                        width: 223
                        height: 31
                        spacing: 1

                        Text {
                            id: txtPhi
                            text: qsTr("phi_0 = ")
                            fontSizeMode: Text.FixedSize
                            font.weight: Font.Medium
                            font.bold: true
                            font.pixelSize: 17
                            lineHeight: 1
                        }

                        Rectangle {
                            id: recPhi
                            width: 80
                            height: 28
                            color: "#ffffff"
                            TextInput {
                                id: phiInput
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                                font.weight: Font.Light
                                font.pixelSize: 17
                                anchors.fill: parent
                                font.family: "Verdana"
                                text: '0'
                            }
                        }
                    }
                }

                Row {
                    id: rowQuiz
                    x: ioFrame.width/2 - rowQuiz.width/4 + 18//285//326
                    y: 150
                    width: 302
                    height: 53
                    spacing: 80


                    Button {
                        id: btnNewQuiz
                        text: qsTr("New Quiz")
                        font.weight: Font.Light

                        onClicked: {

                            // uncheck the cbxShowGuess and clear the signal that indicates the answer
                            cbxShowGuess.checked = false
                            lineSeriesAnsw.clear()
                            txtanswer.text = ''
                            lineSeries.clear()



                            if (actNovice.checked == true) {
                                sindrill.updateXt()
                            }
                            if (actPro.checked == true) {
                                sindrill.updatePro()
                            }

                            var xt = sindrill.xt
                            var tt = sindrill.duration
                            var a = sindrill.A

                            // Reset the inputs & labels
                            phiInput.text = 0
                            f0Input.text = 0
                            amplitudeInput.text = 0
                            txtPeriod.text = "Period = Inf"


                            for (var i = 0; i < xt.length; i++) {

                                lineSeries.append(tt[i]*1000, xt[i])
                            }

                            // Set axisX & axisY
                            axisY.min = -a
                            axisY.max = a
                            axisX.min = tt[0]*1000
                            axisX.max = tt[tt.length - 1]*1000

                            aAnsw.text = 'A = ' + a
                            f0Answ.text = 'f_0 = ' + sindrill.freq
                            phiAnsw.text = 'phi =  ' + sindrill.phi + ' - pi/2'
                        }
                    }

                    CheckBox {
                        id: cbxShowGuess
                        text: qsTr("Show Guess")
                        font.weight: Font.Light
                        indicator.width: 15
                        indicator.height: 15

                        onClicked: {

                            if (cbxShowGuess.checked == true) {
                                var A = amplitudeInput.text
                                var f0 = f0Input.text
                                var phi = phiInput.text
                                 cbxShowGuess.font.bold = true

                                 // Catch the errors !!!
                                 var catchErr = phi.replace('pi', 'Math.PI')
                                 console.log(eval(A))
                                 try {
                                    eval(f0)
                                    eval(A)
                                    eval(catchErr)

                                 } catch (e) {

//                                    console.log(e.message)
                                    phi = '0'
                                    A = '0'
                                    f0 = '0'
                                 }


                                if (axisY.max < parseInt(A)) {
                                    axisY.min = -parseInt(A)
                                    axisY.max = parseInt(A)
                                }

                                // Get value from user
                                sindrill.getvalues(A, f0, phi)

                                // Create signal by user's value.
                                sindrill.updateAnswer()

                                // Get answer and time
                                var answer = sindrill.answer
                                var tt = sindrill.duration
                                for (var i = 0; i < answer.length; i++) {
                                    lineSeriesAnsw.append(tt[i] * 1000, answer[i])
                                }


                                // Show Period ( ms ) & and Answer
                                if (f0 != 0)
                                    txtPeriod.text = "Period = " + (1000/f0).toFixed(2) + " ms"
                                txtanswer.text = A + ' cos ( 2π ' + f0 + ' t ' +' + '+ phi + ' )'

                            }
                            else{
                             cbxShowGuess.font.bold = false
                                lineSeriesAnsw.clear()
                                txtanswer.text = ''

                            }
                        }
                    }
                }

                Rectangle {
                    id: recGuess
                    x: parent.width / 2 - recGuess.width/2
                    y: 8
                    width: 380
                    height: 29
                    color: "#0b7bc1"


                    Text {
                        id: lblGuess
                        color: "#ffffff"
                        text: qsTr("YOUR GUESS")

                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        anchors.fill: parent
                        font.pixelSize: 21
                    }
                }


                Text {
                    id: txtPeriod
                    x: recQuiz.width/2 - 68
                    y: 99
                    width: 102
                    height: 26
                    text: qsTr("Period = Inf")
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: 12
                    font.weight: Font.Light
                    anchors.top: rowInput.bottom
                    anchors.topMargin: -8


                }
            }
        }

        Rectangle {
            id: recAnsw
            width: 50
            height: 20

            anchors.top: ioFrame.bottom
            anchors.topMargin: 20
            x: root.width / 2 - recAnsw.width / 2
            Text {
                id: txtanswer
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.weight: Font.Bold
                font.pixelSize: 17
                color: 'blue'


            }
        }


        Frame {
            id: frameChart
            x: parent.width / 2 - frameChart.width / 2
            y:  320
            width: root.width - 30
            height: root.height - 360
            bottomPadding: -9
            rightPadding: -9
            leftPadding: -9
            topPadding: -9


            ChartView {
                id: chart
                anchors.fill: parent
                legend.visible: false
                antialiasing: true
                animationOptions: ChartView.SeriesAnimations
                theme: ChartView.ChartThemeBlueNcs

                margins.left: 0
                margins.right: 0

                ValueAxis {

                    id: axisY
                }

                ValueAxis {

                    id: axisX
                    tickCount: 9
                }


                LineSeries {
                    id: lineSeries
                    color: "red"
                    axisY: axisY
                    axisX: axisX
                }

                LineSeries {

                    id: lineSeriesAnsw
                    color: "blue"
                    axisY: axisY
                    axisX: axisX
                }


                Component.onCompleted: {

                    sindrill.updateXt()
                    var xt = sindrill.xt
                    var tt = sindrill.duration
                    var a = sindrill.A

                    // Reset the inputs
                    phiInput.text = 0
                    f0Input.text = 0
                    amplitudeInput.text = 0

                    for (var i = 0; i < xt.length; i++) {

                        lineSeries.append(tt[i]*1000, xt[i])
                    }

                    // Set axisX & axisY
                    axisY.min = -a
                    axisY.max = a
                    axisX.min = tt[0]*1000
                    axisX.max = tt[tt.length - 1]*1000

                    aAnsw.text = 'A = ' + a
                    f0Answ.text = 'f_0 = ' + sindrill.freq
                    phiAnsw.text = 'phi =  ' + sindrill.phi + ' - pi/2'

                }

            }// Chart end

        }

        Rectangle {
            id: recTime
            x: frameChart.width/2 - recTime.width/2
            y: 670
            width: 107
            height: 22
            color: "#ffffff"
            anchors.top: frameChart.bottom
            anchors.topMargin: -17


            Label {
                id: lblTime
                text: qsTr("Time  (sec)")
                font.bold: true
                font.pointSize: 11
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
            }
        }

        Rectangle {
            id: recSec
            x: frameChart.width - recSec.width
            y: frameChart.height - recSec.height - 12
            width: 107
            height: 22
            color: "#ffffff"
            anchors.top: frameChart.bottom
            anchors.topMargin: -17

            Label {
                id: time
                text: qsTr("<sub>x10</sub><sup style='font-size:1px;'>-3</sup><")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                font.pointSize: 13
                font.bold: true
                verticalAlignment: Text.AlignVCenter
            }
        }

    }

}
