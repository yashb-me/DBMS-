"""
viz3d.py — Interactive 3D WebGL Visualizers (Three.js) for Database Engine Features.
Includes:
  1. Trigger & Event Pipeline (3D Reactor & Particle Emitter)
  2. B+ Tree Index vs Linear Scan (3D Tree Hierarchy & Traversal Path)
  3. ACID Transaction Stack & Savepoint Ejection (3D Stack & Frame Ejector)
  4. Multi-Dimensional Materialized Cube (3D Voxel Aggregator)
  5. Relational Schema Topology (3D Orbiting Entity-Relationship Graph)
"""

import streamlit.components.v1 as components


def render_trigger_3d(student_id="21BCE1234", status="ABSENT", height=320):
    """3D WebGL Event Pipeline with Particle Flow and Alert Emitter."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background: #F5F5F7; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
        #container {{ width: 100vw; height: {height}px; position: relative; }}
        #toolbar {{
            position: absolute; top: 12px; left: 16px; right: 16px;
            display: flex; justify-content: space-between; align-items: center;
            z-index: 10; pointer-events: none;
        }}
        .tag {{
            background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(8px);
            padding: 5px 12px; border-radius: 9999px; font-size: 11px;
            font-weight: 600; color: #1D1D1F; border: 1px solid #E5E5EA;
            letter-spacing: 0.02em;
        }}
        .btn {{
            pointer-events: auto; background: #0071E3; color: #FFF;
            border: none; border-radius: 9999px; padding: 6px 14px;
            font-size: 11px; font-weight: 500; cursor: pointer;
            box-shadow: 0 2px 6px rgba(0, 113, 227, 0.3); transition: transform 0.15s ease;
        }}
        .btn:hover {{ transform: scale(1.04); background: #0077ED; }}
        .btn:active {{ transform: scale(0.98); }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
    <div id="container">
        <div id="toolbar">
            <span class="tag">3D EVENT-DRIVEN TRIGGER PIPELINE</span>
            <button class="btn" onclick="fireTriggerPulse()">⚡ Trigger Engine Pulse</button>
        </div>
    </div>
    <script>
        const container = document.getElementById('container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xF5F5F7);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 5, 14);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxPolarAngle = Math.PI / 2.1;
        controls.minDistance = 6;
        controls.maxDistance = 25;

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
        dirLight.position.set(5, 12, 8);
        dirLight.castShadow = true;
        scene.add(dirLight);

        const pointLight = new THREE.PointLight(0x0071E3, 2, 20);
        pointLight.position.set(0, 2, 0);
        scene.add(pointLight);

        // Ground Grid
        const grid = new THREE.GridHelper(30, 30, 0xD2D2D7, 0xE5E5EA);
        grid.position.y = -1.5;
        scene.add(grid);

        // Node 1: Input Chamber (DML)
        const nodeMat1 = new THREE.MeshStandardMaterial({{ color: 0xFFFFFF, metalness: 0.1, roughness: 0.2 }});
        const nodeGeo = new THREE.BoxGeometry(2.2, 1.4, 2.2);
        
        const inputNode = new THREE.Mesh(nodeGeo, nodeMat1);
        inputNode.position.set(-5.5, 0, 0);
        inputNode.castShadow = true;
        scene.add(inputNode);

        // Node 2: Trigger Engine Chamber (Center)
        const triggerMat = new THREE.MeshStandardMaterial({{
            color: 0x0071E3, metalness: 0.3, roughness: 0.1, transparent: true, opacity: 0.85
        }});
        const triggerNode = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.5, 1.6, 32), triggerMat);
        triggerNode.position.set(0, 0, 0);
        scene.add(triggerNode);

        // Outer rotating ring for Trigger
        const ringGeo = new THREE.TorusGeometry(2.2, 0.06, 16, 64);
        const ringMat = new THREE.MeshBasicMaterial({{ color: 0x0071E3 }});
        const triggerRing = new THREE.Mesh(ringGeo, ringMat);
        triggerRing.rotation.x = Math.PI / 2;
        scene.add(triggerRing);

        // Node 3: Alert Emitter Pedestal
        const alertMat = new THREE.MeshStandardMaterial({{ color: 0xFF3B30, metalness: 0.2, roughness: 0.3 }});
        const alertNode = new THREE.Mesh(nodeGeo, alertMat);
        alertNode.position.set(5.5, 0, 0);
        alertNode.castShadow = true;
        scene.add(alertNode);

        // Conduits / Tubes connecting nodes
        function createConduit(x1, x2) {{
            const path = new THREE.LineCurve3(new THREE.Vector3(x1, 0, 0), new THREE.Vector3(x2, 0, 0));
            const tubeGeo = new THREE.TubeGeometry(path, 20, 0.12, 8, false);
            const tubeMat = new THREE.MeshStandardMaterial({{ color: 0xD2D2D7, metalness: 0.5, roughness: 0.2 }});
            return new THREE.Mesh(tubeGeo, tubeMat);
        }}
        scene.add(createConduit(-4.4, -1.5));
        scene.add(createConduit(1.5, 4.4));

        // Animated DML Packet
        const packetGeo = new THREE.SphereGeometry(0.35, 32, 32);
        const packetMat = new THREE.MeshStandardMaterial({{ color: 0xFF9500, emissive: 0xFF9500, emissiveIntensity: 0.8 }});
        const packet = new THREE.Mesh(packetGeo, packetMat);
        packet.position.set(-5.5, 1.2, 0);
        scene.add(packet);

        let animating = false;
        let animProgress = 0;

        function fireTriggerPulse() {{
            animProgress = 0;
            animating = true;
            packet.position.set(-5.5, 1.2, 0);
            packetMat.color.setHex(0xFF9500);
            packetMat.emissive.setHex(0xFF9500);
        }}

        function animate() {{
            requestAnimationFrame(animate);

            triggerRing.rotation.z += 0.02;
            triggerNode.rotation.y += 0.01;

            if (animating) {{
                animProgress += 0.02;
                if (animProgress <= 1.0) {{
                    // Stage 1: Move from Input (-5.5) to Trigger (0)
                    packet.position.x = THREE.MathUtils.lerp(-5.5, 0, animProgress);
                    packet.position.y = 1.2 + Math.sin(animProgress * Math.PI) * 0.8;
                }} else if (animProgress <= 1.4) {{
                    // Stage 2: Trigger Chamber Processing
                    triggerNode.scale.set(1.15, 1.15, 1.15);
                    triggerMat.emissive = new THREE.Color(0xFF3B30);
                    triggerMat.emissiveIntensity = 0.6;
                }} else if (animProgress <= 2.4) {{
                    // Stage 3: Alert Packet Ejects to Alert Queue (0 to 5.5)
                    triggerNode.scale.set(1, 1, 1);
                    triggerMat.emissiveIntensity = 0;
                    packetMat.color.setHex(0xFF3B30);
                    packetMat.emissive.setHex(0xFF3B30);
                    const p = (animProgress - 1.4);
                    packet.position.x = THREE.MathUtils.lerp(0, 5.5, p);
                    packet.position.y = 1.2 + Math.sin(p * Math.PI) * 0.8;
                }} else if (animProgress <= 2.8) {{
                    alertNode.position.y = 0.25;
                }} else {{
                    alertNode.position.y = 0;
                    animating = false;
                }}
            }}

            controls.update();
            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }});
    </script>
    </body>
    </html>
    """
    components.html(html, height=height)


def render_btree_3d(search_key="21BCE1234", height=340):
    """3D WebGL B+ Tree vs Sequential Scan Hierarchy."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background: #F5F5F7; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
        #container {{ width: 100vw; height: {height}px; position: relative; }}
        #toolbar {{
            position: absolute; top: 12px; left: 16px; right: 16px;
            display: flex; justify-content: space-between; align-items: center;
            z-index: 10; pointer-events: none;
        }}
        .tag {{
            background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(8px);
            padding: 5px 12px; border-radius: 9999px; font-size: 11px;
            font-weight: 600; color: #1D1D1F; border: 1px solid #E5E5EA;
        }}
        .btn {{
            pointer-events: auto; background: #0071E3; color: #FFF;
            border: none; border-radius: 9999px; padding: 6px 14px;
            font-size: 11px; font-weight: 500; cursor: pointer;
            box-shadow: 0 2px 6px rgba(0, 113, 227, 0.3); transition: transform 0.15s ease;
        }}
        .btn:hover {{ transform: scale(1.04); background: #0077ED; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
    <div id="container">
        <div id="toolbar">
            <span class="tag">B+ TREE 3-HOP TRAVERSAL [O(log N)] VS SEQUENTIAL SCAN [O(N)]</span>
            <button class="btn" onclick="startSearchRace()">▶ Trace Search Path</button>
        </div>
    </div>
    <script>
        const container = document.getElementById('container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xF5F5F7);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 4, 16);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // Lights
        scene.add(new THREE.AmbientLight(0xffffff, 0.9));
        const light = new THREE.DirectionalLight(0xffffff, 0.5);
        light.position.set(0, 10, 10);
        scene.add(light);

        // Ground Grid
        const grid = new THREE.GridHelper(30, 30, 0xD2D2D7, 0xE5E5EA);
        grid.position.y = -3.5;
        scene.add(grid);

        // Node Helper
        function createNode(x, y, z, labelColor = 0xFFFFFF) {{
            const group = new THREE.Group();
            const geo = new THREE.BoxGeometry(1.8, 0.75, 0.8);
            const mat = new THREE.MeshStandardMaterial({{
                color: labelColor, metalness: 0.1, roughness: 0.2
            }});
            const mesh = new THREE.Mesh(geo, mat);
            group.add(mesh);
            group.position.set(x, y, z);
            scene.add(group);
            return mesh;
        }}

        // Conduits
        function linkNodes(p1, p2) {{
            const points = [new THREE.Vector3(p1.x, p1.y - 0.35, p1.z), new THREE.Vector3(p2.x, p2.y + 0.35, p2.z)];
            const geo = new THREE.BufferGeometry().setFromPoints(points);
            const mat = new THREE.LineBasicMaterial({{ color: 0xD2D2D7, linewidth: 2 }});
            scene.add(new THREE.Line(geo, mat));
        }}

        // Level 0: Root Node
        const root = createNode(0, 4, 0, 0x0071E3);

        // Level 1: Internal Branch Nodes
        const b1 = createNode(-4, 1.8, 0);
        const b2 = createNode(0, 1.8, 0);
        const b3 = createNode(4, 1.8, 0);
        linkNodes(root.parent.position, b1.parent.position);
        linkNodes(root.parent.position, b2.parent.position);
        linkNodes(root.parent.position, b3.parent.position);

        // Level 2: Leaf Nodes (Target Leaf is L2)
        const l1 = createNode(-5.5, -0.4, 0);
        const l2 = createNode(-2.5, -0.4, 0);
        const l3 = createNode(0, -0.4, 0);
        const l4 = createNode(2.5, -0.4, 0);
        const l5 = createNode(5.5, -0.4, 0);
        linkNodes(b1.parent.position, l1.parent.position);
        linkNodes(b1.parent.position, l2.parent.position);
        linkNodes(b2.parent.position, l3.parent.position);
        linkNodes(b3.parent.position, l4.parent.position);
        linkNodes(b3.parent.position, l5.parent.position);

        // Sequential Scan Belt at Bottom
        const scanBlocks = [];
        for (let i = 0; i < 16; i++) {{
            const geo = new THREE.BoxGeometry(0.45, 0.35, 0.45);
            const mat = new THREE.MeshStandardMaterial({{ color: 0xE5E5EA }});
            const m = new THREE.Mesh(geo, mat);
            m.position.set(-6 + (i * 0.8), -2.6, 0);
            scene.add(m);
            scanBlocks.push(m);
        }}

        // Traversal Photon Light
        const photon = new THREE.Mesh(
            new THREE.SphereGeometry(0.25, 16, 16),
            new THREE.MeshBasicMaterial({{ color: 0x34C759 }})
        );
        photon.visible = false;
        scene.add(photon);

        function startSearchRace() {{
            photon.visible = true;
            photon.position.set(0, 4, 0);

            // B+ Tree Hop 1 -> Hop 2 -> Hop 3
            root.material.color.setHex(0x34C759);
            setTimeout(() => {{
                root.material.color.setHex(0x0071E3);
                photon.position.set(-4, 1.8, 0);
                b1.material.color.setHex(0x34C759);
            }}, 350);

            setTimeout(() => {{
                b1.material.color.setHex(0xFFFFFF);
                photon.position.set(-2.5, -0.4, 0);
                l2.material.color.setHex(0x34C759);
            }}, 700);

            setTimeout(() => {{
                l2.material.color.setHex(0xFFFFFF);
                photon.visible = false;
            }}, 1200);

            // Sequential crawl on scan tape
            scanBlocks.forEach((block, idx) => {{
                setTimeout(() => {{
                    block.material.color.setHex(0xFF9500);
                    setTimeout(() => block.material.color.setHex(0xE5E5EA), 180);
                }}, idx * 110);
            }});
        }}

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }});
    </script>
    </body>
    </html>
    """
    components.html(html, height=height)


def render_savepoint_3d(height=320):
    """3D WebGL Transaction Frame Stack & Savepoint Ejection."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background: #F5F5F7; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
        #container {{ width: 100vw; height: {height}px; position: relative; }}
        #toolbar {{
            position: absolute; top: 12px; left: 16px; right: 16px;
            display: flex; justify-content: space-between; align-items: center;
            z-index: 10; pointer-events: none;
        }}
        .tag {{
            background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(8px);
            padding: 5px 12px; border-radius: 9999px; font-size: 11px;
            font-weight: 600; color: #1D1D1F; border: 1px solid #E5E5EA;
        }}
        .btn {{
            pointer-events: auto; background: #0071E3; color: #FFF;
            border: none; border-radius: 9999px; padding: 6px 14px;
            font-size: 11px; font-weight: 500; cursor: pointer;
            box-shadow: 0 2px 6px rgba(0, 113, 227, 0.3); transition: transform 0.15s ease;
        }}
        .btn:hover {{ transform: scale(1.04); background: #0077ED; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
    <div id="container">
        <div id="toolbar">
            <span class="tag">TRANSACTION FRAME STACK & CORRUPT BLOCK EJECTION</span>
            <button class="btn" onclick="animateEjection()">↩ Eject Corrupted Frame</button>
        </div>
    </div>
    <script>
        const container = document.getElementById('container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xF5F5F7);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 4, 12);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        scene.add(new THREE.AmbientLight(0xffffff, 0.9));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
        dirLight.position.set(5, 10, 7);
        scene.add(dirLight);

        // Ground Grid
        const grid = new THREE.GridHelper(24, 24, 0xD2D2D7, 0xE5E5EA);
        grid.position.y = -2;
        scene.add(grid);

        // Frame 1: Valid Committed Frame (Bottom)
        const frame1Mat = new THREE.MeshStandardMaterial({{ color: 0x34C759, metalness: 0.1, roughness: 0.2 }});
        const frame1 = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.8, 3.2), frame1Mat);
        frame1.position.set(-2, -1.2, 0);
        scene.add(frame1);

        // Savepoint Checkpoint Pin (Middle Disc)
        const spMat = new THREE.MeshStandardMaterial({{ color: 0xFF9500, metalness: 0.4, roughness: 0.1 }});
        const spMarker = new THREE.Mesh(new THREE.CylinderGeometry(2.4, 2.4, 0.18, 32), spMat);
        spMarker.position.set(-2, -0.6, 0);
        scene.add(spMarker);

        // Frame 2: Corrupted Batch Block (Top)
        const corruptMat = new THREE.MeshStandardMaterial({{ color: 0xFF3B30, metalness: 0.2, roughness: 0.3 }});
        const corruptBlock = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.8, 3.0), corruptMat);
        corruptBlock.position.set(-2, 0.0, 0);
        scene.add(corruptBlock);

        // Final WAL Commited Disk Pedestal (Right)
        const walMat = new THREE.MeshStandardMaterial({{ color: 0x0071E3, metalness: 0.3, roughness: 0.2 }});
        const walPedestal = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.6, 2.2, 32), walMat);
        walPedestal.position.set(4, -0.9, 0);
        scene.add(walPedestal);

        let ejecting = false;
        let t = 0;

        function animateEjection() {{
            t = 0;
            ejecting = true;
        }}

        function animate() {{
            requestAnimationFrame(animate);

            if (ejecting) {{
                t += 0.03;
                if (t <= 1.0) {{
                    // Corrupted block lifts and violently rotates out into void
                    corruptBlock.position.y = 0.0 + (t * 3.5);
                    corruptBlock.position.z = - (t * 4);
                    corruptBlock.rotation.x = t * 1.5;
                    corruptBlock.rotation.y = t * 2.0;
                    corruptMat.opacity = 1 - t;
                    corruptMat.transparent = true;
                }} else if (t <= 1.8) {{
                    // Savepoint rings pulse green
                    spMarker.scale.set(1.1, 1.1, 1.1);
                    spMat.color.setHex(0x34C759);
                }} else {{
                    // Reset to initial state
                    corruptBlock.position.set(-2, 0.0, 0);
                    corruptBlock.rotation.set(0, 0, 0);
                    corruptMat.opacity = 1;
                    corruptMat.transparent = false;
                    spMarker.scale.set(1, 1, 1);
                    spMat.color.setHex(0xFF9500);
                    ejecting = false;
                }}
            }}

            controls.update();
            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }});
    </script>
    </body>
    </html>
    """
    components.html(html, height=height)


def render_materialized_cube_3d(height=320):
    """3D WebGL Multi-Dimensional Department Cube Aggregator."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background: #F5F5F7; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
        #container {{ width: 100vw; height: {height}px; position: relative; }}
        #toolbar {{
            position: absolute; top: 12px; left: 16px; right: 16px;
            display: flex; justify-content: space-between; align-items: center;
            z-index: 10; pointer-events: none;
        }}
        .tag {{
            background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(8px);
            padding: 5px 12px; border-radius: 9999px; font-size: 11px;
            font-weight: 600; color: #1D1D1F; border: 1px solid #E5E5EA;
        }}
        .btn {{
            pointer-events: auto; background: #0071E3; color: #FFF;
            border: none; border-radius: 9999px; padding: 6px 14px;
            font-size: 11px; font-weight: 500; cursor: pointer;
            box-shadow: 0 2px 6px rgba(0, 113, 227, 0.3); transition: transform 0.15s ease;
        }}
        .btn:hover {{ transform: scale(1.04); background: #0077ED; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
    <div id="container">
        <div id="toolbar">
            <span class="tag">INCREMENTAL MATERIALIZED ROUTER [ZERO FULL-TABLE RESCAN]</span>
            <button class="btn" onclick="routeStreamPacket()">⚡ Route Incoming Attendance</button>
        </div>
    </div>
    <script>
        const container = document.getElementById('container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xF5F5F7);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 6, 11);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        scene.add(new THREE.AmbientLight(0xffffff, 0.9));
        const light = new THREE.DirectionalLight(0xffffff, 0.6);
        light.position.set(6, 12, 8);
        scene.add(light);

        // Ground Grid
        const grid = new THREE.GridHelper(24, 24, 0xD2D2D7, 0xE5E5EA);
        grid.position.y = -1.8;
        scene.add(grid);

        // 4 Department Voxels (CSE, ECE, MECH, IT)
        const voxels = [];
        const colors = [0x0071E3, 0x34C759, 0xFF9500, 0xAF52DE];
        const positions = [
            [-2.2, 0, -1.8],
            [1.8, 0, -1.8],
            [-2.2, 0, 1.8],
            [1.8, 0, 1.8]
        ];

        for (let i = 0; i < 4; i++) {{
            const geo = new THREE.BoxGeometry(2.4, 2.2, 2.4);
            const mat = new THREE.MeshStandardMaterial({{
                color: colors[i], metalness: 0.15, roughness: 0.2, transparent: true, opacity: 0.9
            }});
            const mesh = new THREE.Mesh(geo, mat);
            mesh.position.set(...positions[i]);
            scene.add(mesh);
            voxels.push(mesh);
        }}

        // Stream Particle Emitter
        const particle = new THREE.Mesh(
            new THREE.SphereGeometry(0.35, 24, 24),
            new THREE.MeshBasicMaterial({{ color: 0xFFD60A }})
        );
        particle.position.set(-6, 3, 0);
        scene.add(particle);

        let routing = false;
        let rProgress = 0;

        function routeStreamPacket() {{
            rProgress = 0;
            routing = true;
        }}

        function animate() {{
            requestAnimationFrame(animate);

            if (routing) {{
                rProgress += 0.025;
                if (rProgress <= 1.0) {{
                    particle.position.x = THREE.MathUtils.lerp(-6, -2.2, rProgress);
                    particle.position.y = THREE.MathUtils.lerp(3, 1.5, rProgress);
                    particle.position.z = THREE.MathUtils.lerp(0, -1.8, rProgress);
                }} else if (rProgress <= 1.4) {{
                    // Target Voxel (CSE) expands and pulses
                    voxels[0].scale.set(1.15, 1.25, 1.15);
                }} else {{
                    voxels[0].scale.set(1, 1, 1);
                    particle.position.set(-6, 3, 0);
                    routing = false;
                }}
            }}

            controls.update();
            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }});
    </script>
    </body>
    </html>
    """
    components.html(html, height=height)


def render_schema_graph_3d(height=340):
    """3D WebGL Orbiting Relational Entity-Relationship Matrix."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; background: #F5F5F7; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
        #container {{ width: 100vw; height: {height}px; position: relative; }}
        #toolbar {{
            position: absolute; top: 12px; left: 16px; right: 16px;
            display: flex; justify-content: space-between; align-items: center;
            z-index: 10; pointer-events: none;
        }}
        .tag {{
            background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(8px);
            padding: 5px 12px; border-radius: 9999px; font-size: 11px;
            font-weight: 600; color: #1D1D1F; border: 1px solid #E5E5EA;
        }}
        .btn {{
            pointer-events: auto; background: #0071E3; color: #FFF;
            border: none; border-radius: 9999px; padding: 6px 14px;
            font-size: 11px; font-weight: 500; cursor: pointer;
            box-shadow: 0 2px 6px rgba(0, 113, 227, 0.3); transition: transform 0.15s ease;
        }}
        .btn:hover {{ transform: scale(1.04); background: #0077ED; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
    <div id="container">
        <div id="toolbar">
            <span class="tag">3NF NORMALIZED RELATIONAL MATRIX & FOREIGN KEY CONDUITS</span>
            <button class="btn" onclick="pulseFkLinks()">⚡ Pulse Foreign Key Links</button>
        </div>
    </div>
    <script>
        const container = document.getElementById('container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xF5F5F7);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 5, 14);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        scene.add(new THREE.AmbientLight(0xffffff, 0.9));
        const light = new THREE.DirectionalLight(0xffffff, 0.5);
        light.position.set(5, 10, 8);
        scene.add(light);

        // Ground Grid
        const grid = new THREE.GridHelper(26, 26, 0xD2D2D7, 0xE5E5EA);
        grid.position.y = -2.5;
        scene.add(grid);

        // Central Fact Table: attendance
        const centerMat = new THREE.MeshStandardMaterial({{ color: 0x0071E3, metalness: 0.2, roughness: 0.1 }});
        const centerNode = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.4, 2.4), centerMat);
        centerNode.position.set(0, 0, 0);
        scene.add(centerNode);

        // Orbiting Entity Tables: students, subjects, faculty, departments, alerts, warden
        const orbitNodes = [];
        const linkLines = [];
        const tableCount = 6;
        const radius = 5.5;

        for (let i = 0; i < tableCount; i++) {{
            const angle = (i / tableCount) * Math.PI * 2;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;

            const mat = new THREE.MeshStandardMaterial({{ color: 0xFFFFFF, metalness: 0.1, roughness: 0.2 }});
            const node = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.9, 1.6), mat);
            node.position.set(x, 0, z);
            scene.add(node);
            orbitNodes.push(node);

            // Foreign Key Link Line
            const geo = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(0, 0, 0),
                new THREE.Vector3(x, 0, z)
            ]);
            const lineMat = new THREE.LineBasicMaterial({{ color: 0xD2D2D7, linewidth: 2 }});
            const line = new THREE.Line(geo, lineMat);
            scene.add(line);
            linkLines.push(line);
        }}

        function pulseFkLinks() {{
            linkLines.forEach((l) => {{
                l.material.color.setHex(0x34C759);
                setTimeout(() => l.material.color.setHex(0xD2D2D7), 800);
            }});
            centerNode.scale.set(1.2, 1.2, 1.2);
            setTimeout(() => centerNode.scale.set(1, 1, 1), 600);
        }}

        function animate() {{
            requestAnimationFrame(animate);
            centerNode.rotation.y += 0.005;
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }});
    </script>
    </body>
    </html>
    """
    components.html(html, height=height)
