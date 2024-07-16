

def get_extra_data():
    """
    Returns extra data for providers that cannot be automated.
    """
    return extra_data


"""
Fomato de extra_data:
{
    "Provider Name": {
        "field_1": "value_1",
        "field_2": "value_2",
        ...
    },
    ...
"""
extra_data = {
    "IonQ": {
        "website": "https://ionq.com/",
        "description": {
            "short_description": "IonQ specializes in quantum computing using trapped ion technology, offering cloud-based access to their quantum processors.",
            "long_description": "IonQ is at the forefront of quantum computing with its unique trapped ion technology. The company's quantum computers leverage individual ions, which are electrically charged atoms, to function as qubits. This approach offers high levels of stability and coherence, leading to longer qubit operation times and more accurate computations. IonQ provides access to its quantum systems through major cloud platforms like Amazon Web Services (AWS), Microsoft Azure, and Google Cloud, enabling researchers, developers, and businesses to experiment and develop applications in quantum computing.",
            "history": "IonQ was founded in 2015 by Chris Monroe and Jungsang Kim, both pioneers in the field of quantum computing. The company spun out of research conducted at the University of Maryland and Duke University. IonQ quickly established itself as a leader in the quantum space, securing significant funding and partnerships with tech giants. Their technology, based on decades of academic research, continues to push the boundaries of what's possible with quantum computing.",
        },
    },
    "IBM Quantum": {
        "website": "https://www.ibm.com/quantum",
        "description": {
            "short_description": "IBM Quantum offers quantum computing services through cloud access, featuring a suite of quantum computers and development tools for researchers and businesses.",
            "long_description": "IBM Quantum is a division of IBM focused on developing and commercializing quantum computing technology. They provide access to a fleet of quantum processors via the IBM Cloud, alongside a comprehensive software development kit called Qiskit. IBM's quantum systems utilize superconducting qubits and are integrated into a robust quantum ecosystem that includes educational resources, research collaborations, and enterprise solutions. IBM Quantum's platform supports a wide range of quantum algorithms and applications, facilitating advancements in fields such as chemistry, optimization, and machine learning.",
            "history": "IBM has a long history in the field of quantum computing, dating back to the early theoretical work in the 1980s. In 2016, IBM launched the IBM Quantum Experience, making quantum computing available to the public through the cloud for the first time. Since then, IBM has continued to expand its quantum offerings, launching the IBM Q Network in 2017 to foster collaboration with academic, industrial, and government partners. IBM's commitment to quantum computing is reflected in its ongoing research, development, and community-building efforts.",
            "extra": "Check the <a href='https://quantum.ibm.com/services/resources' target='_blank'>IBM Quantum Platform</a> for more information about systems."
        },
    },
    "Rigetti": {
        "website": "https://www.rigetti.com/",
        "description": {
            "short_description": "Rigetti Computing develops and deploys superconducting quantum computers, offering quantum cloud services for various industries and research institutions.",
            "long_description": "Rigetti Computing is a pioneering company in the field of quantum computing, focusing on building and operating superconducting qubit-based quantum processors. The company provides access to its quantum computers through its Quantum Cloud Services (QCS) platform, which integrates classical and quantum computing resources to enable hybrid quantum-classical workflows. Rigetti's approach allows users to develop and run quantum algorithms that can solve complex problems in areas like optimization, materials science, and machine learning.",
            "history": "Rigetti Computing was founded in 2013 by Chad Rigetti, a physicist and former researcher at IBM. The company is headquartered in Berkeley, California, and has rapidly grown to become one of the leading independent quantum computing firms. Rigetti's technological advancements and strategic partnerships have positioned it as a key player in the quantum ecosystem. The company continues to innovate, pushing the envelope with new quantum hardware and software solutions.",
        },
    },
    "Amazon Braket": {
        "website": "https://aws.amazon.com/es/braket/",
        "description": {
            "short_description": "Amazon Braket is a fully managed quantum computing service that provides access to quantum hardware from multiple providers, along with development tools and simulators.",
            "long_description": "Amazon Braket is a quantum computing service offered by Amazon Web Services (AWS). It aims to democratize access to quantum computing by providing a unified platform where users can experiment with quantum computers from different hardware vendors, including Rigetti, IonQ, and D-Wave. Amazon Braket offers a range of tools for developing, testing, and running quantum algorithms, including fully managed Jupyter notebooks, high-performance classical simulators, and integration with other AWS services. This platform enables researchers and developers to explore quantum computing's potential without needing to manage underlying infrastructure.",
            "history": "Launched in December 2019, Amazon Braket represents AWS's strategic entry into the quantum computing space. By collaborating with multiple quantum hardware providers, AWS leverages its extensive cloud infrastructure to offer scalable quantum computing resources. Amazon Braket's launch was part of a broader initiative by AWS to explore emerging technologies and provide innovative solutions to its customers. The service has continued to evolve, adding new features and expanding its ecosystem to support the growing quantum computing community.",
        },
    },
    "QuEra": {
        "website": "https://www.quera.com/",
        "description": {
            "short_description": "QuEra Computing is a quantum computing company focused on developing scalable quantum processors using neutral atom technology.",
            "long_description": "QuEra Computing is a cutting-edge quantum computing startup that employs neutral atom technology to build scalable quantum processors. This approach uses arrays of neutral atoms as qubits, manipulated with highly focused laser beams to perform quantum operations. QuEra's technology aims to overcome some of the scaling challenges faced by other qubit technologies, offering the potential for large, highly connected qubit arrays. The company provides access to its quantum processors for research and commercial applications, aiming to drive innovation in various fields through powerful quantum computations.",
            "history": "Founded in 2019 and based in Boston, Massachusetts, QuEra Computing emerged from groundbreaking research conducted at Harvard University and MIT. The company's founders include renowned physicists and researchers who have made significant contributions to the field of quantum computing. QuEra quickly gained attention for its novel approach and potential for scalable quantum systems. Supported by strong academic ties and venture capital, QuEra is on a path to becoming a significant player in the quantum computing industry.",
        },
    },
}
