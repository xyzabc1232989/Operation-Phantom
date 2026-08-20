new Vue({
    el: '#app',
    data: {
        step: 'landing',
        sessionId: null,
        codename: '',
        phantomId: '',
        currentModule: 1,
        password: '',
        passwordStrength: null,
        typingInput: '',
        keystrokes: [],
        typingMetrics: null,
        behavioral: {
            reuse_passwords: null,
            uses_2fa: null,
            uses_public_wifi: null,
            verifies_links: null,
            uses_password_manager: null
        },
        behavioralResult: null,
        usbDevices: [],
        selectedUSB: null,
        scanningUSB: false,
        scanningFiles: false,
        fileScan: null,
        scanningHidden: false,
        hiddenScan: null,
        scanningDevice: false,
        deviceProfile: null,
        report: null
    },
    methods: {
        async beginAssessment() {
            try {
                const response = await axios.post('/begin', { codename: this.codename || 'SHADOW' });
                this.sessionId = response.data.session_id;
                this.codename = response.data.codename;
                this.phantomId = response.data.phantom_id;
                this.step = 'password';
                this.currentModule = 1;
            } catch (error) {
                console.error('Failed to start assessment:', error);
                alert('Error starting assessment: ' + error.message);
            }
        },
        nextFromRegister() {
            if (this.codename) {
                this.step = 'password';
            }
        },
        async analyzePassword() {
            console.log('Analyzing password:', this.password);
            if (this.password.length === 0) {
                this.passwordStrength = null;
                return;
            }
            try {
                const response = await axios.post('/assess/password', { password: this.password });
                console.log('Password analysis response:', response.data);
                this.passwordStrength = response.data;
            } catch (error) {
                console.error('Password analysis failed:', error);
                alert('Error analyzing password: ' + error.message);
            }
        },
        recordKeyDown(event) {
            this.keystrokes.push({
                key: event.key,
                timestamp: Date.now(),
                type: 'down'
            });
        },
        recordKeyUp(event) {
            this.keystrokes.push({
                key: event.key,
                timestamp: Date.now(),
                type: 'up'
            });
            if (this.typingInput.length === 'CyberSecurity2026'.length && this.typingInput === 'CyberSecurity2026') {
                this.completeTypingAnalysis();
            }
        },
        async completeTypingAnalysis() {
            try {
                const response = await axios.post('/assess/typing', {
                    keystrokes: this.keystrokes,
                    phrase: 'CyberSecurity2026'
                });
                this.typingMetrics = response.data;
            } catch (error) {
                console.error('Typing analysis failed:', error);
            }
        },
        async analyzeBehavioral() {
            try {
                const response = await axios.post('/assess/behavioral', this.behavioral);
                this.behavioralResult = response.data;
                this.nextModule();
            } catch (error) {
                console.error('Behavioral analysis failed:', error);
            }
        },
        async scanUSB() {
            this.scanningUSB = true;
            try {
                const response = await axios.get('/scan/usb');
                this.usbDevices = response.data.devices;
                if (this.usbDevices.length === 0) {
                    alert('No USB devices detected. Please insert a USB drive and try again.');
                }
            } catch (error) {
                console.error('USB scan failed:', error);
            } finally {
                this.scanningUSB = false;
            }
        },
        selectUSB(device) {
            this.selectedUSB = device;
        },
        async scanFiles() {
            if (!this.selectedUSB) return;
            this.scanningFiles = true;
            try {
                const response = await axios.post('/scan/usb/files', { mount_point: this.selectedUSB.mount_point });
                this.fileScan = response.data;
            } catch (error) {
                console.error('File scan failed:', error);
            } finally {
                this.scanningFiles = false;
            }
        },
        async scanHidden() {
            if (!this.selectedUSB) return;
            this.scanningHidden = true;
            try {
                const response = await axios.post('/scan/hidden', { mount_point: this.selectedUSB.mount_point });
                this.hiddenScan = response.data;
            } catch (error) {
                console.error('Hidden file scan failed:', error);
            } finally {
                this.scanningHidden = false;
            }
        },
        async scanDevice() {
            if (!this.selectedUSB) return;
            this.scanningDevice = true;
            try {
                const response = await axios.post('/scan/device', { mount_point: this.selectedUSB.mount_point });
                this.deviceProfile = response.data;
            } catch (error) {
                console.error('Device scan failed:', error);
            } finally {
                this.scanningDevice = false;
            }
        },
        async generateFinalReport() {
            try {
                const response = await axios.post('/generate/report', { 
                    session_id: this.sessionId,
                    password_data: this.passwordStrength,
                    typing_data: this.typingMetrics,
                    behavioral_data: this.behavioralResult,
                    usb_data: { detected: this.usbDevices.length > 0, devices: this.usbDevices },
                    file_scan: this.fileScan
                });
                this.report = response.data;
            } catch (error) {
                console.error('Report generation failed:', error);
            }
        },
        nextModule() {
            console.log('Next module called, current:', this.currentModule);
            console.log('passwordStrength:', this.passwordStrength);
            
            if (this.currentModule === 1 && !this.passwordStrength) {
                alert('Please enter a password to analyze');
                return;
            }
            if (this.currentModule === 2 && !this.typingMetrics) {
                alert('Please complete the typing test');
                return;
            }
            if (this.currentModule === 3 && !this.behavioralResult) {
                alert('Please complete the behavioral assessment');
                return;
            }
            if (this.currentModule === 4 && !this.selectedUSB) {
                alert('Please select a USB device');
                return;
            }
            if (this.currentModule === 7) {
                this.generateFinalReport();
            }
            
            if (this.currentModule < 8) {
                this.currentModule++;
                console.log('Now on module:', this.currentModule);
            }
        },
        prevModule() {
            if (this.currentModule > 1) {
                this.currentModule--;
            }
        },
        resetAssessment() {
            this.step = 'landing';
            this.currentModule = 1;
            this.password = '';
            this.passwordStrength = null;
            this.typingInput = '';
            this.keystrokes = [];
            this.typingMetrics = null;
            this.behavioral = {
                reuse_passwords: null,
                uses_2fa: null,
                uses_public_wifi: null,
                verifies_links: null,
                uses_password_manager: null
            };
            this.usbDevices = [];
            this.selectedUSB = null;
            this.fileScan = null;
            this.hiddenScan = null;
            this.deviceProfile = null;
            this.report = null;
        }
    }
});